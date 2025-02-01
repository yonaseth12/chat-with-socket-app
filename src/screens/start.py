from kivy.utils import platform
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from loading_screen import LoadingScreen
from intro_screen import IntroScreen
from role_choice_screen import RoleChoiceScreen
from server_chat_screen import ServerChatScreen
from client_chat_screen import ClientChatScreen
from help_screen import HelpScreen



class ChatApp(MDApp):
    def build(self):
        # Setting up screen size
        if platform in ('android', 'ios'):
            Window.fullscreen = 'auto'
        else:
            Window.size = (800, 600)
        
        # Setting theme properties
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palatte = 'Teal'
        self.theme_cls.accent_hue = '400'
        self.title = 'Talkie Chat'
        
        # Storing the screens in a list
        screens = [
            LoadingScreen(),
            IntroScreen(),
            RoleChoiceScreen(),
            ServerChatScreen(),
            ClientChatScreen(),
            HelpScreen()
        ]
        
        self.window_manager = ScreenManager(transition=FadeTransition())
        for screen in screens:
            self.window_manager.add_widget(screen)
        
        
        return self.window_manager
    
    
if __name__ == "__main__":
    ChatApp().run()
