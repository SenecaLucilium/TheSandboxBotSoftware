# from macrosWriter import startWriterEvent
# startWriterEvent()
# import keyboard
# keyboard.wait('f8')

import os
import json
from typing import List, Dict, Tuple
from macrosExecutor import replayEvents

def parse_json_events(folder_path: str) -> Tuple[List[Dict], List[Dict]]:
    """Парсит JSON файлы в указанной папке и возвращает два списка ивентов: для клавиатуры и мыши."""
    keyboard_events = []
    mouse_events = []

    with open(os.path.join(folder_path, "keyboard_log.json"), 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list):
            for event in data:
                keyboard_events.append(event)
    with open(os.path.join(folder_path, "mouse_log.json"), 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list):
            for event in data:
                mouse_events.append(event)
    
    return keyboard_events, mouse_events
import keyboard
keyboard.wait('f7')
keyboard_events, mouse_events = parse_json_events("TutorialTest")
replayEvents(keyboard_events, mouse_events)