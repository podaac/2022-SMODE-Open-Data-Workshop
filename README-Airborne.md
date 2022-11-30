# S-MODE DopplerScatt Data Workshop Presentation

[The Sub-Mesoscale Ocean Dynamics Esxperiment (S-MODE)](https://smode.whoi.edu/) is a NASA Earth Ventures mission whose goal is to understand ocean sub-mesoscale; i.e., spatial scales from hundreds of meters to tens of kilometers and temporal scales on the order of days. It is at this scale that it is hypothesized that ocean vertical motions are important for interactions between the ocean and the atmosphere, and for biological productivity.

This repository contains material presented at the [NASA S-MODE Open Data Workshop](https://espo.nasa.gov/s-mode/content/S-MODE_2022_Open_Data_Workshop), held on December 1, 2022. The associated presentation can be found [here.](https://docs.google.com/presentation/d/1YDvMYFJ2zeml2nKaAnssns_CQS2woNWJxBse7dvPZEE/edit?usp=sharing). It demonstrates how to access and visualize DopplerScatt data. DopplerScatt is an airborne Doppler Scatterometer for measuring surface currents and winds.

## Creating a suitable conda environment

The simplest way to run the notebooks in this demonstartion is to use [conda](https://conda.io/projects/conda/en/latest/user-guide/install/download.html) to create a suitable environment:

```shell
conda create -n smode_data_workshop xarray netcdf4 astropy matplotlib jupyterlab
```

## Obtaining DopplerScatt data

### Obtaining an Earthdata account

You can obtain a free NASA Eartdata account by registering here:

https://urs.earthdata.nasa.gov/

### Downloading DopplerScatt data

The [jupyter](https://jupyter.org/) notebook `DownloadingDopplerScattData.ipynb`, located in the notebooks folder, can be used to download DopplerScatt data collected during the S-MODE Pilot campaign.

## Visualizing DopplerScatt data

The notebook `VisualizeDopplerScattData.ipynb` demonstatrates how to read these data and visualize the geophysical measurements, as well as their current limitations.
