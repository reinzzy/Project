from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window

Window.size = (360, 640)

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'keyboard_mode', 'system')

class LoginScreen(Screen):
    def login(self):
        if self.ids.username.text == "admin" and self.ids.password.text == "admin":
            self.show_popup("Login Berhasil", "Selamat datang!")
            self.manager.current = 'main'
        else:
            self.show_popup("Login Gagal", "Username atau password salah!")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))

        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class MainScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class EmployeeListScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(EmployeeListScreen(name='form'))
        return sm

if __name__ == '__main__':
    MyApp().run()
