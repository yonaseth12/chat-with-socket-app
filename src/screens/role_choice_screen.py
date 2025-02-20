from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
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

    selected_card = None

    def select_card(self, choice):
        """Handles card selection with animation."""
        self.selected_card = choice
        
        # Find the selected card
        selected_widget = self.ids.create_group_card if choice == "create" else self.ids.join_group_card
        
        # Animation effect (slight enlargement)
        anim = Animation(size_hint=(0.52, 1.02), duration=0.2) + Animation(size_hint=(0.5, 1), duration=0.2)
        anim.start(selected_widget)

        # Update the UI (to trigger md_bg_color update)
        self.ids.create_group_card.md_bg_color = (.5, 1, 0.5, 0.6) if choice == "create" else (1, 1, 1, 0.2)
        self.ids.join_group_card.md_bg_color = (.5, 1, 0.5, 0.6) if choice == "join" else (1, 1, 1, 0.2)

    def confirm_selection(self):
        """Proceed to the next screen based on selection."""
        if self.selected_card == "join":
            self.manager.current = "join_a_group"
        elif self.selected_card == "create":
            self.manager.current = "create_a_group"  