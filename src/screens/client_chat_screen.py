from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
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
    
    # Clearing All Previous Messages 
    def on_pre_enter(self):
        self.ids.chat_list.clear_widgets()
        
    def on_enter(self):
        self.callback_functions = {
            "receive_message": self.receive_message,
            "user_has_disconnected": self.user_has_disconnected
        }
        app = MDApp.get_running_app()
        app.user_shared_data["user_client"].refer_client_callbacks(self.callback_functions)
        app.user_shared_data["user_client"].start()
        

    def send_message(self):
        message_text = self.ids.message_input.text.strip()
        if message_text:
            
            # Send the message to the server
            app = MDApp.get_running_app()
            app.user_shared_data["user_client"].message_to_send = message_text
            app.user_shared_data["user_client"].sendbtn_pressed = True
            
            
            
        
            # Create a container for each message 
            message_container = MDBoxLayout(
                adaptive_height=True,  
                padding=[10, 8, 15, 8],  # Add spacing inside
                md_bg_color=(0.3, 0.3, 0.3, 1), 
                radius=[10, 10, 0, 10],  
                size_hint_x=None,  # Remove automatic width expansion
                width=self.width * 0.6,  # Explicitly set width to 60% of the parent width
            )

            # Create the message label (multiline + right-aligned text)
            message_label = Label(
                text=message_text,
                size_hint_x=1, 
                halign="right",
                valign="middle",
                color=(1, 1, 1, 1), 
                text_size=(self.width * 0.6 - 20, None),  # Set text wrapping width (subtract padding)
                size_hint_y=None
            )
            message_label.bind(texture_size=message_label.setter("size"))  # Make it multiline

            # Add label to message container
            message_container.add_widget(message_label)

            # Wrap the container inside another box to push it to the right
            outer_box = MDBoxLayout(
                size_hint_x=1,  
                adaptive_height=True,
                padding=[10, 5],  
                md_bg_color=(0, 0, 0, 0)  
            )
            outer_box.add_widget(Widget())  # Add an empty widget for left spacing
            outer_box.add_widget(message_container)  

            self.ids.chat_list.add_widget(outer_box)
            
            # Ensure new messages push previous ones UP instead of appearing at the top
            self.ids.chat_list_container.height = self.ids.chat_list.minimum_height  
            if self.ids.chat_list.height > self.ids.chat_scroll.height:
                # Scroll to the latest message
                Clock.schedule_once(lambda dt: self.ids.chat_list_container.parent.scroll_to(outer_box), 0.1)

            self.ids.message_input.text = ""

    def receive_message(self, message_text):
        if message_text:
            # Create a container for each message 
            message_container = MDBoxLayout(
                adaptive_height=True,  
                padding=[10, 8, 15, 8],  # Add spacing inside
                md_bg_color=(0.3, 0.3, 1, 1), 
                radius=[10, 10, 10, 0],  
                size_hint_x=None,  # Remove automatic width expansion
                width=self.width * 0.6,  # Explicitly set width to 60% of the parent width
            )

            # Create the message label (multiline + left-aligned text)
            message_label = Label(
                text=message_text,
                size_hint_x=1, 
                halign="left",
                valign="middle",
                color=(1, 1, 1, 1), 
                text_size=(self.width * 0.6 - 20, None),  # Set text wrapping width (subtract padding)
                size_hint_y=None
            )
            message_label.bind(texture_size=message_label.setter("size"))  # Make it multiline

            # Add label to message container
            message_container.add_widget(message_label)

            # Wrap the container inside another box to push it to the left
            outer_box = MDBoxLayout(
                size_hint_x=1,  
                adaptive_height=True,
                padding=[10, 5],  
                md_bg_color=(0, 0, 0, 0)  
            )
            outer_box.add_widget(message_container)  
            outer_box.add_widget(Widget())  # Add an empty widget for right spacing

            self.ids.chat_list.add_widget(outer_box)
            
            # Ensure new messages push previous ones UP instead of appearing at the top
            self.ids.chat_list_container.height = self.ids.chat_list.minimum_height  
            if self.ids.chat_list.height > self.ids.chat_scroll.height:
                # Scroll to the latest message
                Clock.schedule_once(lambda dt: self.ids.chat_list_container.parent.scroll_to(outer_box), 0.1)
                
    def user_has_disconnected(self):
        pass
