import RPi.GPIO as GPIO
import os, glob, time, datetime, sys, ConfigParser

# make sure kernal mods are on
os.system('modprobe w1-gpio')   # gpio   
os.system('modprobe w1-therm')  # temp sensor

GPIO.setup(18, GPIO.OUT) # set pin to control
GPIO.output(18, False)   # set pin to false -- starts true

devID = '/sys/bus/w1/devices/28-00000597c7ff/w1_slave';  # file to read from

def read_temp_raw():
    f = open(devID, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


while True:
        temp = read_temp()[0]
        if temp > 27:
            GPIO.output(18, False)
        else:
            GPIO.output(18, True)
        print "Temperature: %sC" % temp
