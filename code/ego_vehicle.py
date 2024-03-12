#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EgoVehicle class definition.

This code was inspired by the one of the SLED dataset (https://github.com/vbrebion/SLED), 
itself inspired by the one of Cooperative Driving Dataset (https://github.com/eduardohenriquearnold/CODD).
"""

import random

import carla
import numpy as np
import queue


class EgoVehicle:
  """The ego-vehicle, which carries all the sensors for the recording"""

  # Class variable, which stores the reference to the unique instance (we want a single ego-vehicle)
  instance = None


  def __init__(self, transform, world, traffic_manager, args):
    """
    Checks first if no other ego-vehicle has already been spawned.
    Then, tries to spawn the ego-vehicle at the given transform (may fail due to collision).
    If it succeeds, then adds all sensors to the vehicle, and sets the instance.
    """

    # We first check if no other ego-vehicle has already been spawned
    if EgoVehicle.instance is not None:
      raise Exception("An ego-vehicle already exists, no new ego-vehicle should be spawned!")

    # We set the random seed
    random.seed = args.seed

    # We try to spawn the ego-vehicle and to configure it
    self.world = world
    self.traffic_manager = traffic_manager
    vehicle_blueprint = world.get_blueprint_library().find('vehicle.tesla.model3')
    vehicle_blueprint.set_attribute('role_name', 'hero')
    self.vehicle = world.try_spawn_actor(vehicle_blueprint, transform)
    if self.vehicle is None:
      raise Exception("Unable to spawn the ego-vehicle at the given transform!")
    self.vehicle.set_autopilot(True, traffic_manager.get_port())
    self.vehicle.set_simulate_physics(True)
    self.traffic_manager.update_vehicle_lights(self.vehicle, True)

    # We create the queue which will hold data from the sensors
    self._queues = []
    self._settings = None

    # We spawn the RGB camera
    rgb_transform = carla.Transform(carla.Location(x=1, z=1.2))
    self.rgb = world.spawn_actor(self.get_rgb_bp(args), rgb_transform, attach_to=self.vehicle)

    # We spawn the semantic camera
    self.semantic = world.spawn_actor(self.get_semantic_bp(args), rgb_transform, attach_to=self.vehicle)

    # We spawn the gnss sensor
    self.gnss = world.spawn_actor(self.get_gnss_bp(args), carla.Transform(), attach_to=self.vehicle)

    # We register the instance
    EgoVehicle.instance = self



  def get_rgb_bp(self, args):
    """Gets and configures the RGB camera blueprint"""
    bp = self.world.get_blueprint_library().find("sensor.camera.rgb")
    rgb_resolution = args.rgb_resolution.split('x')
    bp.set_attribute("image_size_x", rgb_resolution[0])
    bp.set_attribute("image_size_y", rgb_resolution[1])
    bp.set_attribute("fov", args.rgb_fov)
    bp.set_attribute("enable_postprocess_effects", "True") # A set of post-process effects is applied to the image for the sake of realism
    bp.set_attribute("gamma", "2.2") # See https://github.com/carla-simulator/carla/issues/6103
    bp.set_attribute("sensor_tick", "0") # sensor_tick = 0 means as fast as possible
    return bp



  def get_semantic_bp(self, args):
    """Gets and configures the semantic camera blueprint"""
    bp = self.world.get_blueprint_library().find("sensor.camera.semantic_segmentation")
    rgb_resolution = args.rgb_resolution.split('x')
    bp.set_attribute("image_size_x", rgb_resolution[0])
    bp.set_attribute("image_size_y", rgb_resolution[1])
    bp.set_attribute("fov", args.rgb_fov)
    bp.set_attribute("sensor_tick", "0") # sensor_tick = 0 means as fast as possible
    return bp



  def get_gnss_bp(self, args):
    """Gets and configures the RGB camera blueprint"""
    bp = self.world.get_blueprint_library().find("sensor.other.gnss")
    return bp



  def create_queue(self, args):
    """Create the queue for all sensors"""
    self._settings = self.world.get_settings()
    self.frame = self.world.apply_settings(carla.WorldSettings(
      no_rendering_mode=True,
      synchronous_mode=True,
      fixed_delta_seconds=1.0/args.hz))

    def make_queue(register_event):
      q = queue.Queue()
      register_event(q.put)
      self._queues.append(q)

    make_queue(self.world.on_tick)
    for sensor in [self.rgb, self.semantic, self.gnss]:
      make_queue(sensor.listen)
    return self



  def get_sync_data(self, frame):
    """Get the synchronized data for each sensor"""
    self.frame = frame 
    data = [self._retrieve_data(q) for q in self._queues]
    assert all(x.frame == self.frame for x in data) # Checks that the data coming from sensors were generating at the same time. (carla.SensorData.frame returns the frame count when the data was generated.)
    location = self.vehicle.get_location()
    data.append(location)
    return data



  def _retrieve_data(self, sensor_queue):
    while True:
      data = sensor_queue.get()
      if data.frame == self.frame: # Checks that the data coming from sensors were generating at the same time. (carla.SensorData.frame returns the frame count when the data was generated.)
        return data



  def destroy(self):
    """Destroys the sensors and the ego-vehicle"""
    self.rgb.destroy()
    self.semantic.destroy()
    self.gnss.destroy()
    self.vehicle.destroy()
