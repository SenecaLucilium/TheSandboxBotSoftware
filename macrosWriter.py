import keyboard
import time
import json
import os

from cameraEmulator import moveMouseEvent, clickMouseEvent

ARROW_KEYS = {'up', 'down', 'left', 'right'} # Стрелочные клавиши
CLICK_KEYS = {'ctrl', 'alt'} # Клавиши для клика левой и правой кнопки мыши
HOTKEY_PAUSE_RESUME = 'F6' # Клавиша для паузы/возобновления записи
HOTKEY_START_STOP = 'F7' # Клавиша для старта/остановки записи
HOTKEY_EXIT = 'F8' # Клавиша для завершения программы

# Переменные записи
DIR_NAME = None
KEYBOARD_JSON_NAME = 'keyboard_log.json' # НЕ РЕКОМЕНДУЕТСЯ ИЗМЕНЯТЬ - ИМЕЕТ ЗАВИСИМОСТЬ С macrosExecutor.py!
MOUSE_JSON_NAME = 'mouse_log.json' # НЕ РЕКОМЕНДУЕТСЯ ИЗМЕНЯТЬ - ИМЕЕТ ЗАВИСИМОСТЬ С macrosExecutor.py!
MODULE_ACTIVE = True
RECORDING_STARTED = False # Флаг для начала/окончания записи
RECORDING_ACTIVE = False # Флаг для паузы/возобновления записи

# Переменные логов
START_TIME = None
LAST_PAUSE_TIME = None
TOTAL_PAUSED_TIME = None
KEYBOARD_EVENT_LIST = []
MOUSE_EVENT_LIST = []

# Переменная камеры
PIXEL_STEP = 20

def saveEvents() -> None:
    '''Сохраняет записанные ивенты в уже созданные файлы JSON'''
    global DIR_NAME
    with open(os.path.join(DIR_NAME, KEYBOARD_JSON_NAME), "w", encoding='utf-8') as file:
        json.dump(KEYBOARD_EVENT_LIST, file, indent=4, ensure_ascii=False)
    with open(os.path.join(DIR_NAME, MOUSE_JSON_NAME), "w", encoding='utf-8') as file:
        json.dump(MOUSE_EVENT_LIST, file, indent=4, ensure_ascii=False)
    
    print("Events saved.")
    DIR_NAME = None

def hookKeyboard() -> None:
    '''Хукает листенер и добавляет хоткеи'''
    keyboard.add_hotkey(HOTKEY_PAUSE_RESUME, togglePauseResume)
    keyboard.add_hotkey(HOTKEY_START_STOP, toggleStartStop)
    keyboard.add_hotkey(HOTKEY_EXIT, exitModule)
    keyboard.hook(onKeyboardEvent)

def createRecordingDir() -> None:
    '''Создает папку и JSON-файлы для записи.'''
    os.makedirs(DIR_NAME, exist_ok=True)
    keyboard_path = os.path.join(DIR_NAME, KEYBOARD_JSON_NAME)
    mouse_path = os.path.join(DIR_NAME, MOUSE_JSON_NAME)

    open(keyboard_path, 'w').close()
    open(mouse_path, 'w').close()

    print(f"Files created in dir {DIR_NAME}:")
    print(os.listdir(DIR_NAME))

def getRecordingName() -> None:
    '''Получает от пользователя название записи'''
    global DIR_NAME
    while DIR_NAME is None:
        DIR_NAME = input(f'Enter new recording name: ')

        if os.path.exists(DIR_NAME):
            DIR_NAME = None
            print("This directory already exist.")


def togglePauseResume() -> None:
    '''Callback для PAUSE_RESUME_HOTKEY'''
    global RECORDING_ACTIVE, RECORDING_STARTED, LAST_PAUSE_TIME, TOTAL_PAUSED_TIME
    if RECORDING_STARTED is False:
        print("Recording is not started.")
        return
    
    if RECORDING_ACTIVE is True:
        RECORDING_ACTIVE = False
        LAST_PAUSE_TIME = time.time()
        print("Recording paused.")
    else:
        RECORDING_ACTIVE = True
        TOTAL_PAUSED_TIME += time.time() - LAST_PAUSE_TIME
        print("Recording resumed.")

def toggleStartStop() -> None:
    '''Callback для START_STOP_HOTKEY'''
    global RECORDING_STARTED, RECORDING_ACTIVE, DIR_NAME
    global START_TIME, LAST_PAUSE_TIME, TOTAL_PAUSED_TIME, KEYBOARD_EVENT_LIST, MOUSE_EVENT_LIST

    if RECORDING_STARTED is True:
        RECORDING_STARTED = False
        print("Recording stopped.")
        saveEvents()
    else:
        getRecordingName()
        createRecordingDir()
        RECORDING_STARTED = True
        RECORDING_ACTIVE = False

        START_TIME = time.time()
        LAST_PAUSE_TIME = time.time()
        TOTAL_PAUSED_TIME = 0
        KEYBOARD_EVENT_LIST = []
        MOUSE_EVENT_LIST = []

        print(f"Press {HOTKEY_PAUSE_RESUME} to start recording...")

def exitModule() -> None:
    '''Callback для EXIT_HOTKEY'''
    global MODULE_ACTIVE
    MODULE_ACTIVE = False

def onKeyboardEvent(event) -> None:
    '''Функция-хук, которая реагирует на любое нажатие клавиш'''
    global KEYBOARD_EVENT_LIST, MOUSE_EVENT_LIST

    if RECORDING_ACTIVE is False:
        return
    if event.name in {HOTKEY_PAUSE_RESUME, HOTKEY_START_STOP, HOTKEY_EXIT}:
        return
    
    currentTime = time.time()
    timestamp = currentTime - START_TIME - TOTAL_PAUSED_TIME
    
    if event.name in ARROW_KEYS or event.name in CLICK_KEYS:
        MOUSE_EVENT_LIST.append({
            "event": event.event_type,
            "key": event.name,
            "timestamp": timestamp
        })

        if event.name in ARROW_KEYS and event.event_type == 'down':
            moveMouseEvent(event.name, PIXEL_STEP)
        if event.name in CLICK_KEYS:
            clickMouseEvent(event.name, event.event_type)
        return

    KEYBOARD_EVENT_LIST.append({
        "event": event.event_type,
        "key": event.name,
        "timestamp": timestamp
    })

def startWriterEvent() -> None:
    '''Главная функция-ивент: запуск записывающего модуля'''
    print("Recording module is active.")
    while MODULE_ACTIVE:
        hookKeyboard()
        print("Hotkeys:")
        print(f"    {HOTKEY_PAUSE_RESUME}: Pause/Resume recording (while recording)")
        print(f"    {HOTKEY_START_STOP}: Start(create new)/Stop(and save) recording")
        print(f"    {HOTKEY_EXIT}: Exit the program (if recording - without save)")
        
        keyboard.wait(HOTKEY_EXIT)
    print("Recording module is inactive.")