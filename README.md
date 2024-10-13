# The Sandbox Bot Sofrware
## Руководство по использованию

0) Установить необходимые зависимости
```bash
pip install -r requirements.txt
```

1) В корневой папке проекта присутствует файл main.py. В нем написан пример записи и воспроизведения записи

2) Как работает запись:
```python
from macrosWriter import startWriterEvent
startWriterEvent()
```
Запускает модуль записи. В нем самом написан интерфейс взаимодействия. В модуле записи уже встроено создание необходимых папок и файлов.
Во время записи создается папка с тем названием, которое вы задаете. В этой папке будут находится два JSON файла, которые отвечают за события мышки и клавиатуры. Невозможно создать папку с тем именем, которое уже присутствует для избежания конфликтов и ошибок.

3) Как работает воспроизведение:
```python
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
```
Отвечает за воспроизведение записи.
(Т.к. запись сделана модульной с перспективой того, что его можно запускать несколько раз за код - код кривоват)

После запуска этого кода программа будет ждать, пока пользователь нажмет клавишу F7. После этого программа сразу начнет воспроизведение. Рекомендуется нажимать клавишу запуска уже внутри игры, чтобы проигрывание было корректным.

4) Как проиграть запись?
Вставить в корневую папку проекта папку с записью и указать ее название в строчке. В папке обязательно должны присутствовать файлы записи JSON.
```python
keyboard_events, mouse_events = parse_json_events("TutorialTest")
```
В примере это папка TutorialTest.