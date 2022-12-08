# 2022-SMODE-Open-Data-Workshop
December 1, 2022
11am - 1pm ET

The Submesoscale Ocean Dynamics and Vertical Transport Experiment (S-MODE) science team is hosting a virtual Open Data Workshop on 1 December 2022 from 11:00am – 1:00pm ET. We invite everyone in the scientific community to attend this workshop to hear about the S-MODE mission, to learn about its instrumentation, and find out how to access and use its data products.


## Recordings and Presentations

[Presentation materials and a recording of the workshop are available here.](https://espo.nasa.gov/s-mode/content/S-MODE_2022_ODW_Recording_and_Presentations)


## Agenda

(1) Introduction to the S-MODE project, Pilot campaign, and data  
Tom Farrar, Woods Hole Oceanographic Institution - S-MODE Principal Investigator, 20 minutes

(2) Airborne Data Management Group (ADMG) and CASEI inventory (Catalog of Archived Suborbital Earth Science Investigations)  
Deborah Smith, NASA Marshall Space Flight Center, 10 minutes

(3) Introduction/tutorial on S-MODE data sets and cloud data access  
Victoria McDonald and Jack McNelis, NASA JPL - PO.DAAC, 20 minutes

(4) [Science case study #1 - Airborne](#science-case-study-airborne)  
Ernesto Rodriguez, NASA JPL - S-MODE Deputy PI for Airborne Measurements, 30 minutes

(5) [Science case study #2 - In Situ](#science-case-study-in-situ)  
Cesar Rocha, University of Connecticut - Saildrone Principal Investigator, 30 minutes

(6) Wrap up Q&A (10 minutes)


## Prerequisites

To follow along hands-on during the Workshop, please do the following:

### Earthdata Login account

Create an Earthdata Login account (if you don’t already have one) at [https://urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov)
Remember your username and password; you will need to download or access cloud data during the workshop and beyond.

S-MODE datasets can be found through Earthdata Search: [https://search.earthdata.nasa.gov/portal/podaac-cloud/search?fpj=S-MODE](https://search.earthdata.nasa.gov/portal/podaac-cloud/search?fpj=S-MODE)

#### Set up .netrc file for Earthdata login

You will need a netrc file containing your NASA Earthdata Login credentials in order to execute the notebooks. A netrc file can be created manually within text editor and saved to your home directory. An example of the required content is below.

    machine urs.earthdata.nasa.gov
      login <USERNAME>
      password <PASSWORD>

<USERNAME> and <PASSWORD> would be replaced by your actual Earthdata Login username and password respectively.

**NOTE the .netrc file stores your password in plaintext - choose a unique password that is not used for other sensitive logins.**

You can also run the following script to automatically create your .netrc file if it does not yet exist:

    from netrc import netrc
    from subprocess import Popen
    from platform import system
    from getpass import getpass
    import os

    urs = 'urs.earthdata.nasa.gov'    # Earthdata URL endpoint for authentication
    prompts = ['Enter NASA Earthdata Login Username: ',
              'Enter NASA Earthdata Login Password: ']

    # Determine the OS (Windows machines usually use an '_netrc' file)
    netrc_name = "_netrc" if system()=="Windows" else ".netrc"

    # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
    try:
        netrcDir = os.path.expanduser(f"~/{netrc_name}")
        netrc(netrcDir).authenticators(urs)[0]

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        homeDir = os.path.expanduser("~")
        Popen('touch {0}{2} | echo machine {1} >> {0}{2}'.format(homeDir + os.sep, urs, netrc_name), shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]), homeDir + os.sep, netrc_name), shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]), homeDir + os.sep, netrc_name), shell=True)
        # Set restrictive permissions
        Popen('chmod 0600 {0}{1}'.format(homeDir + os.sep, netrc_name), shell=True)

        # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        homeDir = os.path.expanduser("~")
        Popen('echo machine {1} >> {0}{2}'.format(homeDir + os.sep, urs, netrc_name), shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]), homeDir + os.sep, netrc_name), shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]), homeDir + os.sep, netrc_name), shell=True)


## Tutorials and Data Access

S-MODE data can be found through Earthdata Search here: [https://search.earthdata.nasa.gov/portal/podaac-cloud/search?fpj=S-MODE](https://search.earthdata.nasa.gov/portal/podaac-cloud/search?fpj=S-MODE)

The [PO.DAAC Data Downloader](https://github.com/podaac/data-subscriber) can be used to download the datasets used in the following Case Studies. Code can be found in the [notebooks](./notebooks/) directory.

## Science Case Study Airborne

The [DownloadDopplerScattData.ipyb](./notebooks/DownloadDopplerScattData.ipynb) notebook walks through creating the .netrc file and downloading the Dopplerscatt data used in this case study. The [VisualizeDopplerScattData.ipynb](./notebooks/VisualizeDopplerScattData.ipynb) notebook contains the Airborne Science Case Study data visualization and discussion. Instructions for installing the airborne material in a [conda](https://conda.io/projects/conda/en/latest/user-guide/install/download.html) environment are contained in this [Airborne Case Study README](./README-Airborne.md).

## Science Case Study In Situ

The [insitu_datavis_demo.ipynb](./notebooks/insitu_dataviz_demo.ipynb) notebook contains the In Situ Science Case Study data visualization and discussion. This notebook also contains sample code to run the PO.DAAC Data Downloader to download Saildrone data.
Instructions for installing the necessary Python packages, and more information on obtaining S-MODE data are in the [In Situ Case Study README](./README-InSitu.md).ß
