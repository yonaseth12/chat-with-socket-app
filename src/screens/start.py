from kivy.utils import platform
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from screens.loading_screen import LoadingScreen
from screens.intro_screen import IntroScreen
from screens.role_choice_screen import RoleChoiceScreen
from screens.create_a_group_screen import CreateAGroupScreen
from screens.join_a_group_screen import JoinGroupScreen
from screens.server_chat_screen import ServerChatScreen
from screens.client_chat_screen import ClientChatScreen
from screens.help_screen import HelpScreen



class ChatApp(MDApp):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_shared_data = {}
        
    def build(self):
        # Setting up screen size
        if platform in ('android', 'ios'):
            Window.fullscreen = 'auto'
        else:
            Window.size = (300, 600)
        
        # Setting theme properties
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = '400'
        self.title = 'Talkie Chat'
        
        # Storing the screens in a list
        screens = [
            LoadingScreen(name='loading'),
            IntroScreen(name='intro'),
            RoleChoiceScreen(name='role_choice'),
            CreateAGroupScreen(name='create_a_group'),
            JoinGroupScreen(name='join_a_group'),
            ServerChatScreen(name='server_chat'),
            ClientChatScreen(name='client_chat'),
            HelpScreen(name='help')
        ]
        
        self.window_manager = ScreenManager(transition=FadeTransition())
        for screen in screens:
            self.window_manager.add_widget(screen)
        self.window_manager.current = 'loading'
        
        return self.window_manager
    
    
    def go_back(self, previous_page):
        """Go back to the previous screen."""
        self.root.current = previous_page
