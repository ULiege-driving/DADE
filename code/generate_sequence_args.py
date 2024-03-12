#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arguments parser for the sequence generation script.
Allows to configure the simulation.
"""

import argparse
from time import time


def parse_args():
  """Arguments parsing function"""
  argparser = argparse.ArgumentParser()
  argparser.add_argument(
    "--host",
    default="localhost",
    type=str,
    help="IP of the host server (default: localhost)")
  argparser.add_argument(
    "-p", "--port",
    default=2000,
    type=int,
    help="TCP port to listen to (default: 2000)")
  argparser.add_argument(
    "--traffic-manager-port",
    default=8000,
    type=int,
    help="TCP port of CARLA's traffic manager (default: 8000)")
  argparser.add_argument(
    "-m", "--map",
    default="Town12",
    type=str,
    help="Map name (default: Town12)")
  argparser.add_argument(
    "--hz",
    default=10,
    type=float,
    help="The fixed simulation frequency (default: 10.0)")
  argparser.add_argument(
    "--fps",
    default=1,
    type=int,
    help="Number of frames acquired per second (default: 1)")
  argparser.add_argument(
    "--nb_frames",
    type=int,
    default=3600,
    help="Number of frames in the sequence (default: 3600). ")
  argparser.add_argument(
    "--rgb-resolution",
    default="1280x720",
    type=str,
    help="Resolution of the RGB camera and other equivalent sensors (default: 1280x720)")
  argparser.add_argument(
    "--rgb-fov",
    default="90",
    type=str,
    help="FOV of the RGB camera and other equivalent sensors (default: 90°)")
  argparser.add_argument(
    "--nvehicles",
    default=50,
    type=int,
    help="Number of other vehicles in the environment (default: 50)")
  argparser.add_argument(
    "--npedestrians",
    default=50,
    type=int,
    help="Number of pedestrians in the environment (default: 50)")
  argparser.add_argument(
    "--dynamic_weather",
    default="False",
    type=str,
    help="Dynamic weather (default: false)")
  argparser.add_argument(
    "--sun_altitude",
    default=90,
    type=int,
    help="Sun altitude (default: 90 (noon))")
  argparser.add_argument(
    "--cloudiness",
    default=0,
    type=int,
    help="Cloudiness (default: 0 (clear sky))")
  argparser.add_argument(
    "-o", "--output_folder",
    default="dataset",
    type=str,
    help="Name of the created output folder (default: dataset)")
  argparser.add_argument(
    "--csv_file",
    default="dataset/metadata.csv",
    type=str,
    help="Path of the created/updated csv metadata file (default: dataset/metadata.csv)")
  argparser.add_argument(
    "--discard-duration",
    default=3.0,
    type=float,
    help="Duration of the sequence discarded before starting the record (default: 3.0)")
  argparser.add_argument(
    "--seed",
    default=int(time()),
    type=int,
    help="Random seed for reproducibility (default: time.time())")
  return argparser.parse_args()
