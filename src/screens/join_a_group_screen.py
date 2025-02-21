from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
import os
from services.client import Client


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
        popup_label = self.ids.popup_label

        if ip_address and port:
            popup_label.text = f"Joining group at \n{ip_address}:{port}"
            self.show_popup()
            try:
                self.create_client(ip_address, port)
                popup_label.text = "Connected to the group"
                Clock.schedule_once(self.join_client_chat, 3)

            except Exception as e:
                popup_label.text = f"Error: failed to create client connection object. {str(e)[:80]}"
                self.show_popup()
        else:
            popup_label.text = "Please enter an IP address and port number"
            self.show_popup()
    
    def create_client(self, ip_addr, port):
        server_addr = (ip_addr, int(port))
        user_client = Client(server_addr)
        app = MDApp.get_running_app()
        app.user_shared_data = {}
        app.user_shared_data["user_role"] = "client"
        app.user_shared_data["user_client"] = user_client
        
    def join_client_chat(self, dt):
        self.close_popup()
        app = MDApp.get_running_app()
        app.window_manager.current = 'client_chat'
        
    def show_popup(self):
        """Shows the popup when the 'Join Group' button is clicked"""
        popup_label = self.ids.popup_label
        popup_label.text = "\n" + str(popup_label.text)
        popup = self.ids.popup
        popup.opacity = 1

    def close_popup(self):
        """Closes the popup when the 'X' button is clicked"""
        popup = self.ids.popup
        popup.opacity = 0
