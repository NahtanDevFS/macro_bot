import sys
import threading
import shlex  
from pynput import keyboard

from core.recorder import MacroRecorder
from core.engine import MacroPlayer
from core.storage import MacroStorage

class InteractiveMacroBot:
    def __init__(self):
        self.recorder = MacroRecorder()
        self.player = MacroPlayer()
        self.storage = MacroStorage()
        self.recorded_actions = []
        
        self.player.start()
        
        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<f8>': self.toggle_recording,
            '<f9>': self.toggle_playback,
            '<esc>': self.panic
        })

    def toggle_recording(self):
        if self.player._pause_event.is_set():
            print("\n[!] Error: Pause playback before recording.")
            return

        if self.recorder.is_recording:
            self.recorded_actions = self.recorder.stop()
            print(f"\n[*] Recording completed. {len(self.recorded_actions)} actions.")
            print("[Tip] Type 'config' to configure loops or 'save' to save.")
            
            self.player.configure(self.recorded_actions, repeat=1, interval=0)
        else:
            print("\n[*] Recording actions... (Press F8 to stop)")
            self.recorder.start()

    def toggle_playback(self):
        if self.recorder.is_recording: return

        if not self.recorded_actions:
            print("\n[!] No macro loaded.")
            return

        if self.player._pause_event.is_set():
            print("\n[||] Paused.")
            self.player.pause_playing()
        else:
            print(f"\n[>] Playing (Repeat: {self.player.repeat_count}, Interval: {self.player.interval}s)...")
            self.player.start_playing()

    def panic(self):
        print("\n[!!!] EMERGENCY STOP [!!!]")
        if self.recorder.is_recording: self.recorder.stop()
        self.player.stop()
        print("System stopped. Restart the program to use it again.")
        sys.exit(0)

    def cmd_config(self, args):
        if len(args) < 2:
            print("Use: config <repetitions> <interval_seconds>")
            print("infinite example: config -1 2.5")
            print("Example 10 times: config 10 0")
            return
        
        try:
            repeats = int(args[0])
            interval = float(args[1])
            self.player.configure(self.recorded_actions, repeat=repeats, interval=interval)
        except ValueError:
            print("Error: Values ​​must be numbers.")

    def cmd_save(self, args):
        name = args[0] if args else "macro_default.json"
        if not name.endswith(".json"): name += ".json"
        
        if self.recorded_actions:
            self.storage.save(self.recorded_actions, name)
        else:
            print("There are no actions in memory to save.")

    def cmd_load(self, args):
        name = args[0] if args else "macro_default.json"
        if not name.endswith(".json"): name += ".json"
        
        actions = self.storage.load(name)
        if actions:
            self.recorded_actions = actions
            self.player.configure(self.recorded_actions, repeat=1, interval=0)
            print(f"Macro '{name}' loaded. Use 'config' to edit replays.")

    def print_help(self):
        print("\n--- Available Commands ---")
        print(" config <n> <s> : Set up loop (n=-1 infinite, s=waiting seconds)")
        print(" save <name>    : Save macro to file")
        print(" load <name>    : Load macro from file")
        print(" status         : View current settings")
        print(" exit           : EXit")
        print("----------------------------")
        print(" HOTKEYS: [F8] Record | [F9] Play/Pause | [ESC] Panic")

    def start(self):
        self.hotkey_listener.start()
        
        print(">>> Interactive Macro Bot <<<")
        self.print_help()

        while True:
            try:
                user_input = input("\nBot> ").strip()
                if not user_input: continue
                
                parts = shlex.split(user_input)
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == 'exit':
                    print("leaving...")
                    self.player.stop()
                    self.hotkey_listener.stop()
                    sys.exit(0)
                
                elif cmd == 'help':
                    self.print_help()
                
                elif cmd == 'config':
                    self.cmd_config(args)
                
                elif cmd == 'save':
                    self.cmd_save(args)
                
                elif cmd == 'load':
                    self.cmd_load(args)
                
                elif cmd == 'status':
                    print(f"Actions: {len(self.recorded_actions)}")
                    print(f"Config: {self.player.repeat_count} loops | {self.player.interval}s interval")
                
                else:
                    print(f"Unknown command: {cmd}")

            except KeyboardInterrupt:
                self.panic()
            except Exception as e:
                print(f"Command error: {e}")

if __name__ == "__main__":
    app = InteractiveMacroBot()
    app.start()