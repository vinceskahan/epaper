#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# started with waveshare 2in13_V2 demo program
#
# - this assumes the script is in a subdirectory at the same level as 'lib' and 'pic'
#   directories used in the example
#

import sys
import os
from datetime import datetime

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

def get_time():
    return time.strftime('%H:%M:%S')

def get_MQTT_data():
    return "hi there"

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    num = 0
    while (True):

        epd.init(epd.PART_UPDATE)

        # future MQTT display
        #time_draw.text((0,0), get_MQTT_data(), font = font24, fill = 0)

        time_draw.rectangle((0, 0, 220, 105), fill = 255)
        time_draw.text((80,  50), get_time(),  font = font18, fill = 0)

        epd.displayPartial(epd.getbuffer(time_image))

        # clear screen occasionally to prevent burn-in
        now_min = datetime.now().strftime('%M')
        ####print("now_min = %s" % now_min)
        if now_min == '29' or now_min == '00':
            logging.info("cya clear at %s" % now_min)
            epd.init(epd.FULL_UPDATE)
            time_draw.rectangle((0, 0, 220, 105), fill = 255)
            time_draw.text((0,  50), "clearing screen briefly...",  font = font18, fill = 0)
            epd.display(epd.getbuffer(time_image))
            epd.sleep()
            time.sleep(5)
            epd.init(epd.FULL_UPDATE)
            epd.Clear(0xFF)
            epd.init(epd.PART_UPDATE)

        # let it sleep for a bit
        print("quick epd.sleep")
        epd.sleep()
        epd.init(epd.PART_UPDATE)
        print("sleeping 60")
        print()
        time.sleep(60)

        # num = num + 1
        # if(num == 5):
        #     break
        # time.sleep(2)

    epd.Clear(0xFF)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c: doing multiple refreshes to clear ghosting")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    time.sleep(5)
    print("done trying to prevent burnin")
    epd2in13_V2.epdconfig.module_exit()
    exit()
