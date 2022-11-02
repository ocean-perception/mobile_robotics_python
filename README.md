# Mobile robotics python

Placeholder


## How to install

```bash
git clone git@github.com:ocean-perception/mobile_robotics_python.git
cd mobile_robotics_python
pip install -U --user -e .
```

## How to run

In a console, run the following command to print the help.

```bash
mobile_robotics_python -h
```

You should see the following output:
```bash
     ● ●  Ocean Perception
     ● ▲  University of Southampton
 
 Copyright (C) 2022 University of Southampton   
 This program comes with ABSOLUTELY NO WARRANTY.
 This is free software, and you are welcome to  
 redistribute it.                               
 
usage: mobile_robotics_python [-h] [-c CONFIGURATION] [--upload] [--connect] [-v]

Base code for mobile robotics

options:
  -h, --help            show this help message and exit
  -c CONFIGURATION, --configuration CONFIGURATION
                        Configuration file
  --upload              Upload current code to the robot
  --connect             Connect to the robot
  -v, --verbose         Set the verbosity level
```

The program requires you to provide a **configuration file**, which are by default stored at `src/mobile_robotics_python/configuration`. 
 - For mobile robotics, use the file `pitop_robot.yaml`.
 - For maritime robotics, use the file `mrbuild.yaml`.
 
We recommend you to copy the file to you home directory and edit it as you require.

To start the program with your configuration file, you will need to run the following command **in the robot rasbpberry pi**

```bash
mobile_robotics_python -c path/to/configuration/file.yaml
```

## What should I modify to implement a new algorithm?

 - To implement a new localisation driver: use the templates in `src/mobile_robotics_python/localisation_solutions` such as `extended_kalman_filter.py`, `particle_filter.py` or `slam.py`. 
 - To implement a new navigation driver: use the template in `src/mobile_robotics_python/navigation_solutions` named `line_of_sight.py`. 
 - To modify the main robot behaviour: modify the `Robot` class in the file `src/mobile_robotics_python/robot.py`.



### Notes
How to fix IP address: https://www.ionos.co.uk/digitalguide/server/configuration/provide-raspberry-pi-with-a-static-ip-address/ 
Wireless access point: https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
