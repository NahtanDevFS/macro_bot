import time
from pynput import mouse, keyboard
from actions.base import Action
from actions.concrete import ClickAction, WaitAction, KeyPressAction

class MacroRecorder:
    def __init__(self):
        self.actions: list[Action] = []
        self.start_time = None
        self.last_action_time = None
        self.is_recording = False
        
        self.mouse_listener = None
        self.key_listener = None

    def start(self):
        print("--- Starting Recording ---")
        self.actions = []
        self.is_recording = True
        self.start_time = time.time()
        self.last_action_time = self.start_time

        self.mouse_listener = mouse.Listener(
            on_click=self._on_click
        )
        self.key_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

        self.mouse_listener.start()
        self.key_listener.start()

    def stop(self) -> list[Action]:
        print("--- Recording Finished ---")
        self.is_recording = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.key_listener:
            self.key_listener.stop()
            
        return self.actions

    def _record_wait(self):
        if not self.is_recording:
            return

        current_time = time.time()
        delta = current_time - self.last_action_time
        
        if delta > 0.01: 
            self.actions.append(WaitAction(seconds=delta))
        
        self.last_action_time = current_time

    def _on_click(self, x, y, button, pressed):
        if not self.is_recording: return
        
        self._record_wait()
        
        action = ClickAction(x=x, y=y, button=button, pressed=pressed)
        self.actions.append(action)

    def _on_press(self, key):
        if not self.is_recording: return
        
        self._record_wait()
        try:
            char_key = key.char 
            self.actions.append(KeyPressAction(key=char_key, pressed=True))
        except AttributeError:
            self.actions.append(KeyPressAction(key=key, pressed=True))

    def _on_release(self, key):
        if not self.is_recording: return
        
        self._record_wait()
        try:
            char_key = key.char
            self.actions.append(KeyPressAction(key=char_key, pressed=False))
        except AttributeError:
            self.actions.append(KeyPressAction(key=key, pressed=False))