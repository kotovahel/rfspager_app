import time
import datetime
import json


from typing import Literal
from pathlib import Path

def get_previous_messages():
    file_path = Path('../data/messages.json')
    if not file_path.exists():
        file_path.touch(exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('{}')
    with open(file_path, 'r', encoding='utf-8') as f:
        previous_messages = json.loads(f.read())
    return previous_messages

print(get_previous_messages())


