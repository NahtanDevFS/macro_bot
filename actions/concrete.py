import time
from dataclasses import dataclass
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from .base import Action

mouse = MouseController()
keyboard = KeyboardController()

@dataclass
class WaitAction(Action):
    seconds: float

    def execute(self) -> None:
        time.sleep(self.seconds)

@dataclass
class ClickAction(Action):
    x: int
    y: int
    button: Button
    pressed: bool  #true = Press, False = Release 

    def execute(self) -> None:
        mouse.position = (self.x, self.y)
        if self.pressed:
            mouse.press(self.button)
        else:
            mouse.release(self.button)

@dataclass
class KeyPressAction(Action):
    key: str 
    pressed: bool

    def execute(self) -> None:
        if self.pressed:
            keyboard.press(self.key)
        else:
            keyboard.release(self.key)