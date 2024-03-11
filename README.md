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
- semantic segmentation ground-truth masks,
- the GNSS (Global Navigation Satellite System) position of each agent in the simulation,
- the weather information.
All signals are acquired at the framerate of 1 frame per second, with a high-resolution (HD) definition.

We provide code to get the location based on the GNSS data (see the [MSC-TTA repository](https://github.com/ULiege-driving/MSC-TTA)). 

## Downloading

The DADE dataset can be manually downloaded [here](https://dataverse.uliege.be/dataset.xhtml?persistentId=doi:10.58119/ULG/H5SP5P).

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
