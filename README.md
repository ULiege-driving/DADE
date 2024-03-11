# DADE dataset 

## Introduction

The DADE dataset, short for **Driving Agents in Dynamic Environments**, is a synthetic dataset designed for the training and evaluation of methods for the task of semantic segmentation in the context of autonomous driving agents navigating dynamic environments and weather conditions. 

This dataset was generated using the CARLA simulator (version 0.9.14). 

DADE dataset is divided into two sub-datasets: 
- The subset 1, **DADE-static**, is acquired with static weather conditions (clear day) and contains 100 video sequences.
- The subset 2, **DADE-dynamic**, is acquired with varying weather conditions (ranging from day to night, with clear, rainy or foggy conditions) and contains 300 video sequences.
For both subsets, each sequence is acquired by one agent (one ego vehicle) running for some time within a 5-hour time frame, amounting to a total of 990k frames for the entire dataset. The agents travel various locations such as forest, countryside, rural farmland, highway, low density residential, community buildings, and high density residential.

This dataset provides:
- video sequences taken by an RGB camera,
- semantic segmentation ground-truth masks (both from CARLA and the modified version used in our MSC-TTA paper),
- the GNSS (Global Navigation Satellite System) position of each agent in the simulation,
- the weather information.
All signals are acquired at the framerate of 1 frame per second, with a high-resolution (HD) definition.

<div align="center">
<div></div>
  
| **RGB** | **Semantic segmentation ground truths from CARLA** | **Semantic segmentation ground truths used in MSC-TTA** | 
|:----------------:                  |:----------------:                      |:----------------:                |
| <img src="images/000055_img.png">  | <img src="images/000055_sm_carla.png"> | <img src="images/000055_sm.png"> |

</div>

We provide code to get the location based on the GNSS data (see the [MSC-TTA repository](https://github.com/ULiege-driving/MSC-TTA)). 

## Data structure

<pre>
DADE/
├── fixed_weather
│   ├── <i>sequence</i>/ (name of folder: date of the acquisition, for example "2023-07-11_17-35-48")
│   │   ├──semantic_masks/
│   │   │   ├── 001/ (1000 frames per folder)
│   │   │   │   ├── 000001.png
│   │   │   │   ├── 000002.png
│   │   │   │   └── ...
│   │   │   ├── 002
│   │   │   │   ├── 001000.png
│   │   │   │   ├── 001001.png
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── semantic_masks_npz/
│   │   │   ├── 001/
│   │   │   │   ├── 000001.npz
│   │   │   │   ├── 000002.npz
│   │   │   │   └── ...
│   │   │   ├── 002
│   │   │   │   ├── 001000.npz
│   │   │   │   ├── 001001.npz
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── semantic_masks_carla/
│   │   │   ├── 001/
│   │   │   │   ├── 000001.png
│   │   │   │   ├── 000002.png
│   │   │   │   └── ...
│   │   │   ├── 002
│   │   │   │   ├── 001000.png
│   │   │   │   ├── 001001.png
│   │   │   │   └── ...
│   │   │   └── ...
│   │   ├── <i>sequence</i>.mp4
│   │   ├── <i>sequence</i>.json
│   │   └── gnss.json
│   └── ...
├── dynamic_weather
│   ├── <i>sequence</i>/
│   │   ├──semantic_masks/
│   │   ├── semantic_masks_npz/
│   │   ├── semantic_masks_carla/
│   │   ├── <i>sequence</i>.mp4
│   │   ├── <i>sequence</i>.json
│   │   ├── gnss.json
│   │   └── weather.json
├── Town12.png
└── ReadMe.md
</pre>

The `gnss.json` holds a dictionary where the key is the frame number and the value is another dictionary giving the altitude, latitude, longitude, x, y, z values.

The `weather.json` is only present in the dynamic_weather folder and holds a dictionary where the key is the frame number and the value is another dictionary giving the weather parameters values. It gives the cloudiness, fog density, fog distance, fog falloff, mie scattering scale, precipitation, precipitation deposits, rayleigh scattering scale, scattering intensity, sun altitude angle, sun azimuth angle, wetness, and wind intensity. For a definiton of these weather parameters, see the [CARLA documentation](https://carla.readthedocs.io/en/0.9.14/python_api/#carlaweatherparameters). 

The `sequence.json` holds a dictionary with the timestamp randomly attributed to the sequence and the metadata related to this particular sequence. 

`Town12.png` gives based on the x,y coordinates the location in which the agent is. 
The color code is the following one: 

| Zone identifier | Zone name | HEX | RGB |
|:---:|---|:---:|:---:|
| 0 | Forest | 555b19 | (85,91,25) |
| 1 | Countryside | 6fa31b | (111,163,27) |
| 2 | Rural farmland | edc500 | (237,197,0) |
| 3 | Highway | 696e6a | (105,110,106) |
| 4 | Low density residential | 0dd594 | (13,213,148) |
| 5 | Community buildings | 0093e6 | (0,147,230) |
| 6 | High density residential | d52a00 | (213,42,0) |

## Downloading

The DADE dataset can be manually downloaded [here](https://dataverse.uliege.be/dataset.xhtml?persistentId=doi:10.58119/ULG/H5SP5P).

## Generating your own data



## Citation

If you find this dataset useful in your research, please consider citing:

- the DADE dataset:
```bibtex
@data{Halin2023DADE,
  author    = {Halin, Ana\"is and G\'erin, Beno\^it and Cioppa, Anthony and Henry, Maxim and Ghanem, Bernard and Macq, Beno\^it and De Vleeschouwer, Christophe and Van Droogenbroeck, Marc},
  publisher = {ULi\`ege Open Data Repository},
  title     = {{DADE dataset}},
  year      = {2023},
  version   = {V1},
  doi       = {10.58119/ULG/H5SP5P},
  url       = {https://doi.org/10.58119/ULG/H5SP5P}
}
```
- the MSC-TTA paper: 
```bibtex
@article{Gerin2023MultiStream,
  author = {G\'erin, Beno\^it and Halin, Ana\"is and Cioppa, Anthony and Henry, Maxim and Ghanem, Bernard and Macq, Beno\^it and De Vleeschouwer, Christophe and Van Droogenbroeck, Marc},
  title  = {Multi-Stream Cellular Test-Time Adaptation of Real-Time Models Evolving in Dynamic Environments},
  year   = {2023}
}
```

## License
[CC-BY-4.0](https://github.com/ULiege-driving/DADE/blob/main/LICENSE)
