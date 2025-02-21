from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
import os

current_dir = os.path.dirname(__file__) 
kv_path = os.path.join(current_dir, "..", "styles", "client_chat_screen.kv")
kv_path = os.path.normpath(kv_path)
print(f"Loading KV file from: {kv_path}")

try:
    Builder.load_file(kv_path)
    print("KV file loaded successfully!")
except Exception as e:
    print(f"Error loading KV file: {e}")


class ClientChatScreen(Screen):

    def send_message(self):
        """Handles sending messages from input to chat."""
        message = self.ids.message_input.text.strip()
        if message:
            self.ids.chat_list.add_message(message, True)  # True = Sent by user
            self.ids.message_input.text = ""  # Clear input field
     