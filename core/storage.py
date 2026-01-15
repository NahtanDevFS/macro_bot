import json
import os
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
from actions.concrete import ClickAction, WaitAction, KeyPressAction

class MacroStorage:
    @staticmethod
    def save(actions: list, filename: str = "macro.json"):
        data = []
        for action in actions:
            action_dict = {"type": action.__class__.__name__}
            
            if isinstance(action, ClickAction):
                action_dict.update({
                    "x": action.x, "y": action.y, 
                    "button": action.button.name, 
                    "pressed": action.pressed
                })
            elif isinstance(action, KeyPressAction):
                key_val = str(action.key)
                if isinstance(action.key, Key):
                    key_val = f"Key.{action.key.name}" 
                elif isinstance(action.key, KeyCode):
                    key_val = action.key.char 
                
                action_dict.update({"key": key_val, "pressed": action.pressed})
            elif isinstance(action, WaitAction):
                action_dict.update({"seconds": action.seconds})
            
            data.append(action_dict)

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[Storage] Macro saved in {filename}")

    @staticmethod
    def load(filename: str = "macro.json") -> list:
        if not os.path.exists(filename):
            print("[Storage] File not found.")
            return []

        with open(filename, 'r') as f:
            data = json.load(f)

        actions = []
        for item in data:
            type_name = item.pop("type")
            
            if type_name == "WaitAction":
                actions.append(WaitAction(**item))
            
            elif type_name == "ClickAction":
                item["button"] = getattr(Button, item["button"]) 
                actions.append(ClickAction(**item))
            
            elif type_name == "KeyPressAction":
                k_str = item["key"]
                if k_str.startswith("Key."):
                    key_name = k_str.split(".")[1]
                    item["key"] = getattr(Key, key_name)
                else:
                    item["key"] = KeyCode.from_char(k_str) if len(k_str) == 1 else k_str
                
                actions.append(KeyPressAction(**item))
        
        print(f"[Storage] {len(actions)} loaded actions.")
        return actions