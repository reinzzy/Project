from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window
from screen.login_screen import LoginScreen
from screen.signup_screen import SignupScreen
from screen.main_screen import MainScreen
from screen.profile_screen import ProfileScreen
from screen.employeelist_screen import EmployeeListScreen
from screen.absensi_screen import AbsensiScreen

Window.size = (360, 640)

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'keyboard_mode', 'system')

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(EmployeeListScreen(name='form'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(AbsensiScreen(name='absensi'))
        return sm

if __name__ == '__main__':
    MyApp().run()
