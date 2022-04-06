#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# started with waveshare 2in13_V2 demo program
#
# - this assumes the script is in a subdirectory at the same level as 'lib' and 'pic'
#   directories used in the example
#

import argparse
from datetime import datetime
import os
import paho.mqtt.client as mqtt
import requests
import sys

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

# default logging level is 'WARNING' 
#   levels are CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET high to low
#   INFO is a little more verbose
#   DEBUG is more verbose than INFO

logging.basicConfig(level=logging.ERROR)

def get_time():
    return time.strftime('%I:%M %p')

def get_weather():
    try:
        # this file is written by weewx on a computer on the LAN
        # so just grab the results and pick off the temperature
        weather = requests.get('http://192.168.1.128/weewx/current.html').text.split()
        temp = weather[2] + " F"
        return temp
    except: 
        return "unavailable"

def display_it():
    try:
        epd = epd2in13_V2.EPD()
        logging.info("init and Clear")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing on the image
        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
    
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(time_image))
    
        num = 0
        while (True):

            epd.init(epd.PART_UPDATE)
            time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)

            time_draw.text((80,  20), get_weather(), font = font32, fill = 0)
            time_draw.text((85, 105), get_time(),    font = font18, fill = 0)

            epd.displayPartial(epd.getbuffer(time_image))

            # clear screen occasionally to prevent burn-in
            now_min = datetime.now().strftime('%M')
            if now_min == '29' or now_min == '59':
                logging.info("cya clear at %s" % now_min)
                epd.init(epd.FULL_UPDATE)
                time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)
                time_draw.text((0,  50), "clearing screen briefly...",  font = font18, fill = 0)
                epd.display(epd.getbuffer(time_image))
                epd.sleep()
                time.sleep(5)
                epd.init(epd.FULL_UPDATE)
                epd.Clear(0xFF)
                epd.init(epd.PART_UPDATE)

            # let it sleep for a bit
            logging.info("quick epd.sleep")
            epd.sleep()
            epd.init(epd.PART_UPDATE)
            logging.info("sleeping 60")
            time.sleep(60)

        epd.Clear(0xFF)
        logging.info("Clear...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        clear_it()

def clear_it():
        logging.info("ctrl + c: doing multiple refreshes to clear ghosting")

        logging.info("  1 of 5")
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        time.sleep(5)
        logging.info("  2 of 5")
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        time.sleep(5)
        logging.info("  3 of 5")
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        time.sleep(5)
        logging.info("  4 of 5")
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        time.sleep(5)
        logging.info("  5 of 5")
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        time.sleep(5)
        logging.info("done trying to prevent burnin")
        epd2in13_V2.epdconfig.module_exit()
        exit()

if __name__ == "__main__":

    # argument parsing is u.g.l.y it ain't got no alibi, it's ugly !
    #   the epilog prints after the long help if you add the -h or --help option
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        """,
    )

    parser.add_argument("-c", "--clear", dest="clear", action="store_true", help="clear screen to prevent burn-in")

    args = parser.parse_args()

    if (args.clear):
            clear_it()
            sys.exit(0)

    # this will call the weather data too
    display_it()


#############

sys.exit(0)

