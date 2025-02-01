from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
import os


kv_path = os.path.join(os.path.dirname(__file__), "../styles/intro_screen.kv")
Builder.load_file(kv_path)


class IntroScreen(Screen):
    pass