from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os


current_dir = os.path.dirname(__file__) 
kv_path = os.path.join(current_dir, "..", "styles", "join_a_group_screen.kv")
kv_path = os.path.normpath(kv_path)
print(f"Loading KV file from: {kv_path}")

try:
    Builder.load_file(kv_path)
    print("KV file loaded successfully!")
except Exception as e:
    print(f"Error loading KV file: {e}")


class JoinGroupScreen(Screen):
    def join_group(self):
        ip_address = self.ids.ip_input.text
        port = self.ids.port_input.text

        if ip_address and port:
            print(f"Joining group at {ip_address}:{port}")
            # You can add validation and networking logic here
