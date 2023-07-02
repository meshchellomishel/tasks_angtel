#!/usr/bin/python3


import evdev as ev
import time
import json
from threading import Thread
from pprint import pprint


def read_keyboard(data, device):
    for event in device.read_loop():
        if event.type == ev.ecodes.EV_KEY:
            cat_event = ev.categorize(event)
            data += [{"Type": "EV_KEY", "Code": cat_event.keycode, "State": cat_event.keystate}]


def read_mouse(data, device):
    for event in device.read_loop():
        if event.type == ev.ecodes.EV_ABS:
            cat_event = ev.categorize(event).event
            data += [{"Type": "EV_ABS", "Value": cat_event.value}]


def end_prog():
    file = open(FILE_NAME, 'w')
    json.dump(data, file, indent=True)
    pprint(data)


if __name__ == "__main__":
    MOSE_EVENT = 'event10'
    KEYBOARD_EVENT = 'event2'
    FILE_NAME = 'output.txt'
    data = []

    keyboard = ev.InputDevice(f"//dev//input//{KEYBOARD_EVENT}")
    mouse_ev = ev.InputDevice(f"//dev//input//{MOSE_EVENT}")

    keyboard_reader = Thread(target=read_keyboard, args=(data, keyboard,), daemon=True)
    mouse_reader = Thread(target=read_mouse, args=(data, mouse_ev,), daemon=True)
    
    try:
        keyboard_reader.start()
        read_mouse(data, mouse_ev)
    except KeyboardInterrupt:
        end_prog()
