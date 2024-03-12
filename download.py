#!/usr/bin/env python

"""
Download script for DADE dataset.

The data is released under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License.

Script usage example:
    python download.py  --dade  "all" \         # subset to download. Options: "static", "dynamic", or "all" 
                        dataset_root            # path where to store the downloaded data

"""

import argparse
import os
import sys
import wget
import tarfile

BASE_URL = "https://dataverse.uliege.be/api/access/datafile/"

README_URL = "28017"
TOWN12_URL = "28012"
STATIC_URL = "28010"
DYNAMIC_1_URL = "28014"
DYNAMIC_2_URL = "28015"
DYNAMIC_3_URL = "28016"

def main():
    parser = argparse.ArgumentParser(description="Downloads DADE dataset.")
    parser.add_argument("out_dir", help="output directory in which to store the data.")
    parser.add_argument("--dade", type=str, default="all", choices=["static", "dynamic", "all"], help="subset to download.")
    args = parser.parse_args()

    print("Thank you for downloading DADE dataset! \n")

    dataset_dir = os.path.join(args.out_dir, "DADE")
    if not os.path.isdir(dataset_dir):
        os.makedirs(dataset_dir)
    
    if not os.path.isfile(os.path.join(dataset_dir,"ReadMe.md")):
        print("Downloading ReadMe.md")
        url = BASE_URL + README_URL
        wget.download(url, os.path.join(dataset_dir,"ReadMe.md"))

    if not os.path.isfile(os.path.join(dataset_dir,"Town12.png")):
        print("\n Downloading Town12.png")
        url = BASE_URL + TOWN12_URL
        wget.download(url, os.path.join(dataset_dir,"Town12.png"))

    if args.dade == "static" or "all": # != "dynamic"
        if not os.path.isfile(os.path.join(dataset_dir,"static_weather.tar")):
            print("\n Downloading static_weather.tar")
            url = BASE_URL + STATIC_URL
            wget.download(url, os.path.join(dataset_dir,"static_weather.tar"))
            print("\n Extracting static_weather.tar")
            with tarfile.open(os.path.join(dataset_dir,"static_weather.tar")) as tar:
                tar.extractall(path=dataset_dir)
            os.remove(os.path.join(dataset_dir,"static_weather.tar"))
        
    
    if args.dade == "dynamic" or "all": # != "static"
        dynamic_dir = os.path.join(dataset_dir,"dynamic_weather")
        if not os.path.isdir(dynamic_dir):
            os.makedirs(dynamic_dir)
        if not os.path.isfile(os.path.join(dataset_dir,"dynamic_weather_part1.tar")):
            print("\n Downloading dynamic_weather_part1.tar")
            url = BASE_URL + DYNAMIC_1_URL
            wget.download(url, os.path.join(dataset_dir,"dynamic_weather_part1.tar"))
            print("\n Extracting dynamic_weather_part1.tar")
            with tarfile.open(os.path.join(dataset_dir,"dynamic_weather_part1.tar")) as tar:
                tar.extractall(path=dynamic_dir)
            os.remove(os.path.join(dataset_dir,"dynamic_weather_part1.tar"))
        if not os.path.isfile(os.path.join(dataset_dir,"dynamic_weather_part2.tar")):
            print("\n Downloading dynamic_weather_part2.tar")
            url = BASE_URL + DYNAMIC_2_URL
            wget.download(url, os.path.join(dataset_dir,"dynamic_weather_part2.tar"))
            print("\n Extracting dynamic_weather_part2.tar")
            with tarfile.open(os.path.join(dataset_dir,"dynamic_weather_part2.tar")) as tar:
                tar.extractall(path=dynamic_dir)
            os.remove(os.path.join(dataset_dir,"dynamic_weather_part2.tar"))
        if not os.path.isfile(os.path.join(dataset_dir,"dynamic_weather_part3.tar")):
            print("\n Downloading dynamic_weather_part3.tar")
            url = BASE_URL + DYNAMIC_3_URL
            wget.download(url, os.path.join(dataset_dir,"dynamic_weather_part3.tar"))
            print("\n Extracting dynamic_weather_part3.tar")
            with tarfile.open(os.path.join(dataset_dir,"dynamic_weather_part3.tar")) as tar:
                tar.extractall(path=dynamic_dir)
            os.remove(os.path.join(dataset_dir,"dynamic_weather_part3.tar"))

    print("Done!")


if __name__ == "__main__":
    main()
