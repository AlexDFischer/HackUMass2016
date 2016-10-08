import RPi.GPIO as GPIO
import socket
import time
import string
import math

global urPin
global ulPin
global lrPin
global llPin

global urPwm
global ulPwm
global lrPwm
global llPwm

global boardSideLength
global pulleyRadius

def setup():
	global urPin
	global ulPin
	global lrPin
	global llPin
	
	global urPwm
	global ulPwm
	global lrPwm
	global llPwm
	
	global boardSideLength
	global pulleyRadius
	global port
	global ipToAccept
	ipToAccept = "72.19.72.216"
	# set pin numbers
	urPin = 12
	ulPin = 11
	lrPin = 16
	llPin = 15
	# set up pins to PWM output
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(urPin, GPIO.OUT)
	GPIO.setup(ulPin, GPIO.OUT)
	GPIO.setup(lrPin, GPIO.OUT)
	GPIO.setup(llPin, GPIO.OUT)
	urPwm = GPIO.PWM(urPin, 50)
	ulPwm = GPIO.PWM(ulPin, 50)
	lrPwm = GPIO.PWM(lrPin, 50)
	llPwm = GPIO.PWM(llPin, 50)
	urPwm.start(7.5)
	ulPwm.start(7.5)
	lrPwm.start(7.5)
	llPwm.start(7.5)
	# board dimensions constants
	boardSideLength = 500.0 # side length in millimeters
	pulleyRadius = 20.0 # pulley radius in millimeters
	# networking constants
	port = 8080
def handleRollPitch(roll, pitch):
	roll = roll / 10.0
	pitch = pitch / 10.0
	urHeight = boardSideLength/2.0*(pitch+roll)
	ulHeight = boardSideLength/2.0*(pitch-roll)
	lrHeight = boardSideLength/2.0*(-pitch+roll)
	llHeight = boardSideLength/2.0*(-pitch-roll)
	# these angles are from neutral, ie from 90 degrees
	urAngle = urHeight/pulleyRadius
	ulAngle = ulHeight/pulleyRadius
	lrAngle = lrHeight/pulleyRadius
	llAngle = llHeight/pulleyRadius
	urDutyCycle = 7.5 + 2.5*urAngle/(math.pi/2)
	ulDutyCycle = 7.5 + 2.5*ulAngle/(math.pi/2)
	lrDutyCycle = 7.5 + 2.5*lrAngle/(math.pi/2)
	llDutyCycle = 7.5 + 2.5*llAngle/(math.pi/2)
	urPwm.ChangeDutyCycle(urDutyCycle)
	ulPwm.ChangeDutyCycle(ulDutyCycle)
	lrPwm.ChangeDutyCycle(lrDutyCycle)
	llPwm.ChangeDutyCycle(llDutyCycle)
	print "ur=%2.2f ul=%2.2f lr=%2.2f ll=%2.2f" % (urHeight, ulHeight, lrHeight, llHeight)
if __name__ == "__main__":
	setup()
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind(("", port))
	serversocket.listen(5)
	while True:
		(clientsocket, address) = serversocket.accept()
		print "someone connected to me"
		file = clientsocket.makefile()
		firstline = file.readline()
		firstline = ''.join(filter(lambda c: c in string.printable, firstline)) # filters out non printable characters, from stack overflow
		print "firstline is " + str(firstline)
		while True:
			line = file.readline()
			linesplit = line.split(",")
			roll = float(linesplit[0])
			pitch = float(linesplit[1])
			handleRollPitch(roll, pitch)
