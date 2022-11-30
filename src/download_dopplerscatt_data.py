"""Functions for accessing DopplerScatt data from PODAAC."""

from netrc import netrc
from subprocess import Popen
from platform import system
from getpass import getpass
import os
from subprocess import run
import shlex


def download_dopplerscatt_data(
        data_dir='../data/SMODE_L2_DOPPLERSCATT_WINDS_CURRENT_V1',
        start_date='2021-11-03T00:00:00Z',
        end_date='2021-11-04T00:00:00Z',
        downloader='podaac-data-downloader'):
    """Download S-MODE DopplerScatt data from PODAAC."""
    s = f'{downloader} -c SMODE_L2_DOPPLERSCATT_WINDS_CURRENT_V1 -d {data_dir}  --start-date {start_date} --end-date {end_date}'
    status = run(shlex.split(s))
    if status.returncode == 0:
        print('Succesfully downloaded desired DopplerScatt data.')
    else:
        print(
            f'Downloading desired DopplerScatt data exited with status {status}'
        )


def setup_netrc_file():
    """PODAAC recipe for setting up netrc file for data downloads.

    Recipe obtained from PODAAC here:

    https://nasa-openscapes.github.io/earthdata-cloud-cookbook/get-started/earthdata-login.html
    """
    urs = 'urs.earthdata.nasa.gov'  # Earthdata URL endpoint for authentication
    prompts = [
        'Enter NASA Earthdata Login Username: ',
        'Enter NASA Earthdata Login Password: '
    ]

    # Determine the OS (Windows machines usually use an '_netrc' fi
    netrc_name = "_netrc" if system() == "Windows" else ".netrc"
    homeDir = os.path.expanduser("~")

    # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
    try:
        netrcDir = os.path.expanduser(f"~/{netrc_name}")
        netrc(netrcDir).authenticators(urs)[0]
        print('valid netrc file found')

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        print('netrc file not found, please login into NASA Earthdata:')
        Popen('touch {0}{2} | echo machine {1} >> {0}{2}'.format(
            homeDir + os.sep, urs, netrc_name),
              shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]),
                                             homeDir + os.sep, netrc_name),
              shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]),
                                                    homeDir + os.sep,
                                                    netrc_name),
              shell=True)
        # Set restrictive permissions
        Popen('chmod 0600 {0}{1}'.format(homeDir + os.sep, netrc_name),
              shell=True)

        print(f'nterc file written to {homeDir}{os.sep}{netrc_name}')

        # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        print(
            'netrc exists but is not set up for NASA Earthdata Login, please login into NASA Earthdata:'
        )
        homeDir = os.path.expanduser("~")
        Popen('echo machine {1} >> {0}{2}'.format(homeDir + os.sep, urs,
                                                  netrc_name),
              shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]),
                                             homeDir + os.sep, netrc_name),
              shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]),
                                                    homeDir + os.sep,
                                                    netrc_name),
              shell=True)

        print(f'nterc file written to {homeDir}{os.sep}{netrc_name}')

    return f'{homeDir}{os.sep}{netrc_name}'
