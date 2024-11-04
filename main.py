import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from kivy.core.window import Window
from screen.login_screen import LoginScreen
from screen.signup_screen import SignupScreen
from screen.main_screen import MainScreen
from screen.profile_screen import ProfileScreen
from screen.employeelist_screen import EmployeeListScreen
from screen.absensi_screen import AbsensiScreen
from screen.addgaji_screen import AddGaji
from screen.cekgaji_screen import CekGaji
from screen.resetpw_screen import ResetPasswordScreen
from screen.user_screen import UserScreen
from screen.attendance_screen import AttendanceScreen

Window.size = (360, 640)
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'keyboard_mode', 'system')

kv_dir = os.path.join(os.path.dirname(__file__), 'kivy')
for kv_file in os.listdir(kv_dir):
    if kv_file.endswith('.kv'):
        Builder.load_file(os.path.join(kv_dir, kv_file))

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(EmployeeListScreen(name='form'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(AbsensiScreen(name='absensi'))
        sm.add_widget(AddGaji(name='addgaji'))
        sm.add_widget(CekGaji(name='cekgaji'))
        sm.add_widget(ResetPasswordScreen(name='resetpw'))
        sm.add_widget(UserScreen(name='user_absen'))
        sm.add_widget(AttendanceScreen(name='attendance'))
        return sm

if __name__ == '__main__':
    MyApp().run()
