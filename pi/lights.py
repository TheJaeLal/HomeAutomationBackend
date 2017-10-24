import RPi.GPIO as GPIO ## Import GPIO library
import sys

led_pins = [7, 11]

control = sys.argv[1].strip().upper()=='ON' 
no = int(sys.argv[2])

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(led_pins[no], GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(led_pins[no],control)