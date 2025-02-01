from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
import os

current_dir = os.path.dirname(__file__) 
kv_path = os.path.join(current_dir, "..", "styles", "loading_screen.kv")
kv_path = os.path.normpath(kv_path)
print(f"Loading KV file from: {kv_path}")

try:
    Builder.load_file(kv_path)
    print("KV file loaded successfully!")
except Exception as e:
    print(f"Error loading KV file: {e}")

class LoadingScreen(Screen):
    def on_enter(self):
        print("LoadingScreen entered. Transitioning in 3 seconds...")
        Clock.schedule_once(self.switch_to_intro, 3)

    def switch_to_intro(self, dt):
        if self.manager:
            print("Switching to IntroScreen...")
            self.manager.current = "intro"
        else:
            print("Error: ScreenManager is not set!")
