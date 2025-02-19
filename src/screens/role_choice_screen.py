from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
import os


current_dir = os.path.dirname(__file__) 
kv_path = os.path.join(current_dir, "..", "styles", "role_choice_screen.kv")
kv_path = os.path.normpath(kv_path)
print(f"Loading KV file from: {kv_path}")

try:
    Builder.load_file(kv_path)
    print("KV file loaded successfully!")
except Exception as e:
    print(f"Error loading KV file: {e}")

class RoleChoiceScreen(Screen):
    def create_group(self):
        pass
    def join_group(self):
        pass