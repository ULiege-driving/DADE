#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script can be used to generate a single sequence in the CARLA simulator, containing:
- images from a RGB camera (.png);
- semantic segmentation ground truths (.png);
- geolocalisation data (.json).
The sequence is saved in a folder.

This code was inspired by the one of the SLED dataset (https://github.com/vbrebion/SLED), 
itself inspired by the one of Cooperative Driving Dataset (https://github.com/eduardohenriquearnold/CODD).
"""

import csv
import random
from time import sleep
from datetime import datetime
import os

import carla
import json
from tqdm import tqdm

from ai_pedestrian import AIPedestrian
from ai_vehicle import AIVehicle
from ego_vehicle import EgoVehicle
from dynamic_weather import Weather
from generate_sequence_args import parse_args


def main():
  """Main function"""

  # We begin by collecting the command-line args
  args = parse_args()
  hz = args.hz
  if args.hz < args.fps:
    hz = args.fps

  # We set the random seed
  random.seed(args.seed)

  # We connect to the CARLA simulator
  client = carla.Client(args.host, args.port)
  client.set_timeout(300.0)

  # We load the correct map
  world = client.load_world(args.map)

  # We apply the simulation settings
  settings = world.get_settings()
  settings.synchronous_mode = True
  settings.fixed_delta_seconds = 1.0/hz
  if args.map == "Town12":
    settings.tile_stream_distance = 2000   # Set the streaming distance so tiles will be loaded within a 2km radius of the ego vehicle
    settings.actor_active_distance = 2000 # Set the actor active distance to a 2 km radius around the ego vehicle (Actors will become dormant 2km away from the ego vehicle)
  world.apply_settings(settings)

  # We configure the traffic manager
  traffic_manager = client.get_trafficmanager(args.traffic_manager_port)
  traffic_manager.set_synchronous_mode(True)
  traffic_manager.set_random_device_seed(args.seed)
  traffic_manager.set_hybrid_physics_mode(True) # This enables hybrid mode for the TM
  traffic_manager.set_hybrid_physics_radius(100)
  if args.map == "Town12":
    traffic_manager.set_respawn_dormant_vehicles(True) # This enables respawning of dormant vehicles within 100 and 500 meters of the hero vehicle
    traffic_manager.set_boundaries_respawn_dormant_vehicles(100,500)


  # We configure the time and weather settings
  # We draw a random timestamp 
  seq_timestamp = random.randint(-3600, 18000-1)
  if seq_timestamp < 0 :
    seq_timestamp = 0
  elif seq_timestamp > 16199 :
    seq_timestamp = 16199
  dynamic_weather = args.dynamic_weather
  if dynamic_weather == 'True' or dynamic_weather == 'true': 
    print('The weather is dynamic.')
    # We instantiate a Weather class
    weather = Weather(world.get_weather(), seq_timestamp)
    world.set_weather(weather.weather)
    # We initialize the timer for the sequence
    elapsed_time = 0.0
    # We get the light manager
    light_manager = world.get_lightmanager()
  else : # If the weather is fixed
    weather = carla.WeatherParameters.ClearNoon
    weather.sun_altitude_angle = args.sun_altitude
    weather.cloudiness = args.cloudiness
    world.set_weather(weather)

  # We spawn the ego-vehicle
  ego_vehicle_transform = random.choice(world.get_map().get_spawn_points())
  ego_vehicle = EgoVehicle(ego_vehicle_transform, world, traffic_manager, args)

  # We spawn the other AI-controlled vehicles
  while(len(AIVehicle.instances) < args.nvehicles):
    vehicle_transform = random.choice(world.get_map().get_spawn_points())
    AIVehicle(vehicle_transform, world, traffic_manager, args)

  # We spawn the AI-controlled pedestrians
  while(len(AIPedestrian.instances) < args.npedestrians):
    pedestrian_location = world.get_random_location_from_navigation()
    pedestrian_transform = carla.Transform(location=pedestrian_location)
    AIPedestrian(pedestrian_transform, world, args)

  # We compute the number of world ticks we have to discard and to record, based on the durations
  # given by the user
  ticks_to_discard = int(args.discard_duration * hz)
  ticks_to_record = int(args.nb_frames * hz / args.fps)

  # We create the queues, which will hold the numpy arrays of data before saving them to disk
  rgb_images_queue = []
  semantic_images_queue = []
  gnss_dic = {}
  weather_dic = {}

  nb_frames_saved = 0
  dir_name = 1
  save_frame = False
  counter_frame = 0
  folder_name = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
  
  # Save metadata in csv file
  with open(args.csv_file, 'a', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=';')
      csv_writer.writerow([folder_name, args.map, args.seed, args.dynamic_weather, args.sun_altitude, args.cloudiness, args.nvehicles, args.npedestrians, seq_timestamp])
      csv_file.close()

  # Save metadata of the sequence in json file
  if not os.path.exists('{}/{}'.format(args.output_folder, folder_name)):
    os.makedirs('{}/{}'.format(args.output_folder, folder_name))
  dic = {"timestamp":seq_timestamp, "map":args.map, "seed":args.seed, "dynamic_weather":args.dynamic_weather, "nb_vehicles":args.nvehicles, "nb_pedestrians":args.npedestrians, "seq_length":"NaN"}
  with open('{}/{}/{}.json'.format(args.output_folder, folder_name, folder_name), 'w') as fp:
    json.dump(dic, fp, indent=4)


  try:
    # We compute a first world tick, after which we can enable the controller of the pedestrians
    world.tick()
    for pedestrian in AIPedestrian.instances:
      pedestrian.start_controller()

    ego_vehicle.create_queue(args)

    # We loop a first time, to skip the first world ticks that should be discarded
    for _ in tqdm(range(ticks_to_discard), "Discarding ticks"):
      frame = world.tick()

      # We already update the weather and light status so that when we record the first frame, it's ready
      if dynamic_weather == 'True' or dynamic_weather == 'true': # We update the weather 
        elapsed_time += 1.0/hz
        if seq_timestamp+elapsed_time > 18000:
          break
        weather.tick(seq_timestamp+elapsed_time)
        world.set_weather(weather.weather)
        # We turn off or on the lights depending on the sun altitude angle
        if weather.weather.sun_altitude_angle < 1 :
          light_manager.set_active(light_manager.get_all_lights(), [True for i in range(len(light_manager.get_all_lights()))])
        else :
          light_manager.set_active(light_manager.get_all_lights(), [False for i in range(len(light_manager.get_all_lights()))])

      # Remove data from the queue without saving them
      snapshot, rgb_image, semantic_image, gnss_data, location = ego_vehicle.get_sync_data(frame)

    # We then loop until we reach the end of the simulation
    for _ in tqdm(range(ticks_to_record), "Recording ticks"):
      frame = world.tick()

      if dynamic_weather == 'True' or dynamic_weather == 'true': # We update the weather 
        elapsed_time += 1.0/hz
        weather.tick(seq_timestamp+elapsed_time)
        world.set_weather(weather.weather)
        # We turn off or on the lights depending on the sun altitude angle
        if weather.weather.sun_altitude_angle < 1 :
          light_manager.set_active(light_manager.get_all_lights(), [True for i in range(len(light_manager.get_all_lights()))])
        else :
          light_manager.set_active(light_manager.get_all_lights(), [False for i in range(len(light_manager.get_all_lights()))])

      # Save data at args.fps frequency 
      save_frame = False
      if counter_frame%(hz/args.fps) == 0:
        nb_frames_saved +=1
        save_frame = True
        counter_frame = 0

      # We check that the sequence does not go over the 5h timeframe
      if seq_timestamp+nb_frames_saved > 18000:
          break

      # Save 1000 files per folder
      if nb_frames_saved%1000 == 0 and counter_frame%(hz/args.fps) == 0:
        dir_name += 1

      counter_frame += 1

      # Get data from the queue
      snapshot, rgb_image, semantic_image, gnss_data, location = ego_vehicle.get_sync_data(frame)

      # Save data
      if save_frame:
        rgb_image.save_to_disk("{}/{}/images/{:03d}/{:06d}.png".format(args.output_folder, folder_name, dir_name, nb_frames_saved))
        semantic_image.convert(carla.ColorConverter.CityScapesPalette)
        semantic_image.save_to_disk("{}/{}/semantic_masks/{:03d}/{:06d}.png".format(args.output_folder, folder_name, dir_name, nb_frames_saved))
        gnss_dic[nb_frames_saved] = {"latitude":gnss_data.latitude, "longitude":gnss_data.longitude, "altitude":gnss_data.altitude, "x":location.x, "y":location.y, "z":location.z}  
        # Save GNSS data in a json file
        with open('{}/{}/gnss.json'.format(args.output_folder, folder_name), 'w') as fp:
          json.dump(gnss_dic, fp, sort_keys=True, indent=4)
        if dynamic_weather == 'True' or dynamic_weather == 'true':
          weather_dic[nb_frames_saved] = {"sun_azimuth_angle":weather.weather.sun_azimuth_angle, "sun_altitude_angle":weather.weather.sun_altitude_angle, "cloudiness":weather.weather.cloudiness, "precipitation":weather.weather.precipitation, 
                                          "precipitation_deposits":weather.weather.precipitation_deposits, "wind_intensity":weather.weather.wind_intensity, "fog_density":weather.weather.fog_density, "fog_distance":weather.weather.fog_distance, 
                                          "fog_falloff":weather.weather.fog_falloff, "wetness":weather.weather.wetness, "scattering_intensity":weather.weather.scattering_intensity, "mie_scattering_scale":weather.weather.mie_scattering_scale, 
                                          "rayleigh_scattering_scale":weather.weather.rayleigh_scattering_scale}  
          # Save weather data in a json file
          with open('{}/{}/weather.json'.format(args.output_folder, folder_name), 'w') as fp:
            json.dump(weather_dic, fp, sort_keys=True, indent=4)

  # At the end (or if anything goes wrong), we remove all the vehicles/pedestrians from the
  # simulation
  finally:
    ego_vehicle.destroy()
    for vehicle in AIVehicle.instances:
      vehicle.destroy()
    for pedestrian in AIPedestrian.instances:
      pedestrian.destroy()

  # And for some reason, we have to wait for a few seconds to avoid having the process crashing with
  # a "terminate called without an active exception" error
  sleep(5)


if __name__ == "__main__":
  main()
