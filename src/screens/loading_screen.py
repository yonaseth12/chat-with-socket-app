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
        
        # List of animated texts to cycle through
        self.loading_texts = ["Loading", "Loading.", "Loading..", "Loading..."]
        self.current_index = 0
        
        # Update the label every 0.5 seconds
        Clock.schedule_interval(self.update_text, 1)
        
        Clock.schedule_once(self.switch_to_intro, 5)
        

    def switch_to_intro(self, dt):
        if self.manager:
            print("Switching to IntroScreen...")
            self.manager.current = "intro"
        else:
            print("Error: ScreenManager is not set!")

    def update_text(self, dt):
        # Update the text of the MDLabel using its id
        self.ids.loading_label.text = self.loading_texts[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.loading_texts)