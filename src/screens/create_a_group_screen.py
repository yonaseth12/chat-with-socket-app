from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from services.server import Server
import os


current_dir = os.path.dirname(__file__) 
kv_path = os.path.join(current_dir, "..", "styles", "create_a_group_screen.kv")
kv_path = os.path.normpath(kv_path)
print(f"Loading KV file from: {kv_path}")

try:
    Builder.load_file(kv_path)
    print("KV file loaded successfully!")
except Exception as e:
    print(f"Error loading KV file: {e}")

    
class CreateAGroupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_server()
        
    def create_server(self):
        user_server = Server()
        app = MDApp.get_running_app()
        app.user_shared_data["user_role"] = "server"
        app.user_shared_data["user_server"] = user_server
        

    def on_enter(self):
        self.message = ""
        
        self.ids.loading_label.text = self.message
        self.loading_texts = ["Creating", "Creating.", "Creating..", "Creating..."]
        self.current_index = 0
        
        Clock.schedule_interval(self.update_text, 1)


    def update_screen(self, dt):
        # Update the UI after 3 seconds
        app = MDApp.get_running_app()
        server_addr = app.user_shared_data["user_server"].ADDR
        self.ids.loading_label.text = f"Your group is now ready!\n Invite your friends with \nIP   {server_addr[0]} \nPort  {server_addr[1]}"
        self.ids.enter_button.opacity = 1
        self.ids.enter_button.disabled = False
        
        
        
    def update_text(self, dt):
        # Update the text of the MDLabel using its id
        self.ids.loading_label.text = self.loading_texts[self.current_index]
        self.current_index = self.current_index + 1 
        if self.current_index == len(self.loading_texts):
            Clock.unschedule(self.update_text)
            Clock.schedule_once(self.update_screen, 1)