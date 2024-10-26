from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import os

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/user.kv')
Builder.load_file(kv_path)

class UserScreen(Screen):
    def go_to_attendance(self):
        self.manager.current = 'attendance'

    def set_user_id(self, user_id):
        self.user_id = user_id
