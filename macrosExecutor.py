import keyboard
import time
import json
import os

from cameraEmulator import moveMouseEvent, clickMouseEvent

ARROW_KEYS = {'up', 'down', 'left', 'right'} # Стрелочные клавиши
CLICK_KEYS = {'ctrl', 'alt'} # Клавиши для клика левой и правой кнопки мыши
PIXEL_STEP = 20

def replayEvents(keyboardEvents, mouseEvents) -> None:
    '''Проигрывает все действия в хронологическом порядке'''

    allEvents = sorted(keyboardEvents + mouseEvents, key=lambda e: e["timestamp"])
    startTime = time.time()

    for event in allEvents:
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        waitTime = event["timestamp"] - elapsedTime

        if waitTime > 0:
            time.sleep(waitTime)
        print (event["key"])
        if event["key"] in ARROW_KEYS and event["event"] == "down":
            moveMouseEvent(event["key"], PIXEL_STEP)
        elif event["key"] in CLICK_KEYS:
            clickMouseEvent(event["key"], event["event"])
        else:
            if event["event"] == "down":
                keyboard.press(event["key"])
            elif event["event"] == "up":
                keyboard.release(event["key"])