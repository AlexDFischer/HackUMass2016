import RPi.GPIO as GPIO
import socket
import time
import string
import math

global rollPin
global pitchPin

global rollPwm
global pitchPwm

def setup():
	global rollPin
	global pitchPin
	
	global rollPwm
	global pitchPwm
	global port
	global ipToAccept
	ipToAccept = "72.19.72.216"
	# set pin numbers
	pitchPin = 11
	rollPin = 12
	# set up pins to PWM output
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pitchPin, GPIO.OUT)
	GPIO.setup(rollPin, GPIO.OUT)
	pitchPwm = GPIO.PWM(pitchPin, 50)
	rollPwm = GPIO.PWM(rollPin, 50)
	pitchPwm.start(7.5)
	rollPwm.start(7.5)
	# networking constants
	port = 8080
def handleRollPitch(roll, pitch):
	roll = roll / 2
	pitch = pitch / 2
	# don't let it turn more than 45 degrees
	pitchmin = -math.pi / 4
	pitchmax = math.pi / 4
	rollmin = -math.pi / 4
	rollmax = math.pi / 4
	if (pitch < pitchmin):
		pitch = pitchmin
	elif pitch > pitchmax:
		pitch = pitchmax
	if (roll < rollmin):
		roll = rollmin
	elif (roll > rollmax):
		roll = rollmax
	# these angles are from neutral, ie from 90 degrees
	pitchDutyCycle = 7.5 + 2.5*pitch/(math.pi/4)
	rollDutyCycle = 7.5 + 2.5*roll/(math.pi/4)
	pitchPwm.ChangeDutyCycle(pitchDutyCycle)
	rollPwm.ChangeDutyCycle(rollDutyCycle)
	print "pitch=%2.0f roll=%2.0f" % (pitch*180/math.pi, roll*180/math.pi)
if __name__ == "__main__":
	setup()
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
