 ## Import GPIO library
import RPi.GPIO as GPIO

led_pins = [7, 11]

#light_no is an interger 0 or 1
#Control is a boolean, True or False
def control(light_no,control):
	global led_pins
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	GPIO.setup(led_pins[light_no], GPIO.OUT) ## Setup GPIO Pin 7 to OUT
	GPIO.output(led_pins[light_no],control)

#Returns a dictionary of Response
def get_status():
	global led_pins

	response = {"1":"OFF","2":"OFF"}
	
	if GPIO.input(led_pins[0]):
		response["1"] = "ON"
	if GPIO.input(led_pins[1]):
		response["2"] = "ON"

	return response