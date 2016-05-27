import RPi.GPIO as GPIO
import time
import atexit
import threading

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(15,1)

def flashLights(arg1, stop_event):
	print "Flashing"
	x = 0
	while(not stop_event.is_set()):
		y = x % 2
		GPIO.output(11 + y,1)
		GPIO.output(12 - y,0)
		x = x + 1
		time.sleep(0.1)

def stopFlashing():
	GPIO.output(11,0)
	GPIO.output(12,0)

def progExit():
	GPIO.cleanup()

atexit.register(progExit)

btn_prev_state = 0
lightsonoff = 0

while 1:
	input = GPIO.input(16)
	if (input and input != btn_prev_state):
		btn_prev_state = input
		if (not lightsonoff):
			print "On"
			stop_event = threading.Event()
			thread = threading.Thread(target = flashLights, args=(1,stop_event))
			thread.start()
			lightsonoff = 1
		else:
			print "Off"
			stop_event.set()
			lightsonoff = 0
			stopFlashing
	else:
		btn_prev_state = input
		
