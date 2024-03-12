#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script can be used to generate the full dataset in the CARLA simulator, composed of
N sequences, each containing:
- images from a RGB camera (.png);
- semantic segmentation ground truths (.png);
- geolocalisation data (.json).
Each sequence is saved in a folder.

This code was inspired by the one of the SLED dataset (https://github.com/vbrebion/SLED), 
itself inspired by the one of Cooperative Driving Dataset (https://github.com/eduardohenriquearnold/CODD).
"""

import argparse
import csv
from datetime import datetime
from os.path import exists
import random
import subprocess


def parse_args():
  """Arguments parsing function"""
  argparser = argparse.ArgumentParser()
  argparser.add_argument(
    "--nb_seq",
    type=int,
    default=1,
    help="Number of sequences to randomly generate (default: 1). ")
  argparser.add_argument(
    "--nb_frames",
    type=int,
    default=3600,
    help="Number of frames in each sequence (default: 3600). ")
  argparser.add_argument(
    "--fps",
    type=int,
    default=1,
    help="Number of frames acquired per second (default: 1). ")
  argparser.add_argument(
    "--map",
    type=str,
    default="Town12",
    help="CARLA map in which the data must be acquired (default: Town12). ")
  argparser.add_argument(
    "--dynamic_weather",
    default="False",
    type=str,
    help="Dynamic weather (default: False)")
  argparser.add_argument(
    "--output_folder",
    type=str,
    default="dataset",
    help="Path to the folder where generated sequences will be saved (default: dataset)")
  return argparser.parse_args()


def main():
  """Main function"""

  # We begin by collecting the command-line args
  args = parse_args()

  nb_seq_to_generate = args.nb_seq
  nb_frames_in_seq = args.nb_frames
  fps = args.fps
  dynamic_weather = args.dynamic_weather

  # We initialize the list of maps
  maps = [f"Town0{i}" for i in range(1, 8)] + ["Town10HD"] + ["Town12"]

  # For each of the N sequences...
  for i in range(nb_seq_to_generate):
    # Display progress to the user
    print(f"Generating sequence {i+1}/{nb_seq_to_generate}...")

    # We select a seed based on current date and time, and select a map based on it if no map was chosen.
    seed = datetime.now().strftime("%Y%m%d_%H%M%S")
    random.seed(seed)
    if args.map != "":
      map = args.map
      if map not in maps:
        raise Exception(f"Map {map} is not part of the list of maps!")
    else:
      map = random.choice(maps)

    # We set the adequate output folder and csv file names
    output_folder = f"{args.output_folder}"
    csv_file = f"{args.output_folder}/metadata.csv"

    # And we finally call the sequence generation script with the args
    subprocess.run(["python3", "generate_sequence.py", "--map", map, "--seed", seed, 
      "--fps", str(fps), "--nb_frames", str(nb_frames_in_seq), "--npedestrians", str(0),
      "--dynamic_weather", str(dynamic_weather), "--output_folder", output_folder, "--csv_file", csv_file], check=True)


if __name__ == "__main__":
  main()
