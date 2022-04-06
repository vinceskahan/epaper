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

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

def get_time():
    return time.strftime('%H:%M:%S')

def get_MQTT_temp(broker,topic):
    return "42.5 degF"

def get_MQTT_gust(broker,topic):
    return "13 mph"

def get_MQTT_rain(broker,topic):
    return "0.13 in"

def display_it(broker,topic):
    try:
        logging.info("epd2in13_V2 Demo")
    
        epd = epd2in13_V2.EPD()
        logging.info("init and Clear")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing on the image
        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(time_image))
    
        num = 0
        while (True):

            epd.init(epd.PART_UPDATE)
            time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)

            # future MQTT display
            time_draw.text((80,0),  get_MQTT_temp(broker,topic), font = font24, fill = 0)
            time_draw.text((100,50), get_MQTT_gust(broker,topic), font = font18, fill = 0)
            time_draw.text((100,70), get_MQTT_rain(broker,topic), font = font18, fill = 0)
            # reasonably centered
            #     time_draw.text((80,  50), get_time(),  font = font18, fill = 0)
            # bottom row
            time_draw.text((100,  105), get_time(),  font = font15, fill = 0)

            epd.displayPartial(epd.getbuffer(time_image))

            # clear screen occasionally to prevent burn-in
            now_min = datetime.now().strftime('%M')
            if now_min == '29' or now_min == '12':
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
            print("quick epd.sleep")
            epd.sleep()
            epd.init(epd.PART_UPDATE)
            print("sleeping 60")
            print()
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
        print("done trying to prevent burnin")
        epd2in13_V2.epdconfig.module_exit()
        exit()

def setup_mqtt(mqtt_broker,mqtt_topic):
        print("mqtt=%s mqtt_broker=%s topic=%s" % (args.mqtt, args.mqtt_broker, args.mqtt_topic))

if __name__ == "__main__":

    # argument parsing is u.g.l.y it ain't got no alibi, it's ugly !
    #   the epilog prints after the long help if you add the -h or --help option
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        """,
    )

    parser.add_argument("-m", "--mqtt", dest="mqtt", action="store_true", help="listen for MQTT data")
    parser.add_argument("-b", "--mqtt_broker", dest="mqtt_broker", action="store", help="MQTT broker hostname")
    parser.add_argument("-t", "--mqtt_topic",  dest="mqtt_topic",  action="store", help="MQTT topic to post to")

    parser.add_argument("-d", "--dry_run", dest="dry_run", action="store_true", help="dry_run - show what you 'would' do")

    args = parser.parse_args()

    if (args.mqtt) or (args.mqtt_broker) or (args.mqtt_topic):
        if (not args.mqtt) or (not args.mqtt_broker) or (not args.mqtt_topic):
            print ("\n# exiting - must also specify --mqtt_broker and -mqtt_topic")
            parser.print_usage()
            print ()
            sys.exit(1)

    if args.mqtt_broker:
        MQTT_HOST = args.mqtt_broker

    if args.mqtt_topic:
        MQTT_TOPLEVEL_TOPIC = args.mqtt_topic

    if args.dry_run:
        print()
        print("mqtt=%s mqtt_broker=%s topic=%s" % (args.mqtt, args.mqtt_broker, args.mqtt_topic))
        print()
        print("done")
    else:
        if args.mqtt:
            setup_mqtt(args.mqtt_broker,args.mqtt_topic)
        display_it(args.mqtt_broker,args.mqtt_topic)


#############

sys.exit(0)

