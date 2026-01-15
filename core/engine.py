import threading
import time
from typing import List
from actions.base import Action
from actions.concrete import WaitAction

class MacroPlayer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._actions: List[Action] = []
        
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.clear() 
        
        self.repeat_count = 1   # 1 = once, -1 = infinite
        self.interval = 0.0     
        self.current_loop = 0

    def configure(self, actions: List[Action], repeat: int = 1, interval: float = 0.0):
        self._actions = actions
        self.repeat_count = repeat
        self.interval = interval
        self.current_loop = 0
        print(f"[Engine] Configured: {len(actions)} actions | Repeat: {repeat} | Interval: {interval}s")

    def run(self):
        print("--- Playback Engine Ready ---")
        
        while not self._stop_event.is_set():
            self._pause_event.wait()
            
            if self._stop_event.is_set(): break

            while self.repeat_count == -1 or self.current_loop < self.repeat_count:
                
                if self._stop_event.is_set() or not self._pause_event.is_set():
                    break 

                print(f"--- Running Loop {self.current_loop + 1} ---")
                
                for action in self._actions:
                    if self._stop_event.is_set(): return
                    
                    while not self._pause_event.is_set():
                        time.sleep(0.1)
                        if self._stop_event.is_set(): return

                    if isinstance(action, WaitAction):
                        time.sleep(action.seconds)
                    else:
                        try:
                            action.execute()
                        except Exception as e:
                            print(f"Error: {e}")
                
                self.current_loop += 1
                
                if self.interval > 0:
                    print(f"[Engine] Waiting {self.interval}s for the next cycle...")
                    time.sleep(self.interval)

            print("--- Cycles completed. On hold. ---")
            self.current_loop = 0
            self._pause_event.clear()

    def start_playing(self):
        self._pause_event.set()

    def pause_playing(self):
        self._pause_event.clear()

    def stop(self):
        self._stop_event.set()
        self._pause_event.set()