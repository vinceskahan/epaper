#!/usr/bin/bash
#

# this assumes nohup.out 'here' is a symlink to /dev/null
cd /home/pi/e-Paper/RaspberryPi_JetsonNano/python/bin

# activate the pyenv and nohup the script
source /home/pi/e-Paper/bin/activate && nohup python3 /home/pi/e-Paper/RaspberryPi_JetsonNano/python/bin/epaper.py &

# alternately run the system python if it has had the requirements installed
#nohup python3 /home/pi/e-Paper/RaspberryPi_JetsonNano/python/bin/epaper.py &

