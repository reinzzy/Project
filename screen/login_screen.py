import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/login.kv')
Builder.load_file(kv_path)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.current_user_uid = None

    def login(self):
        email = self.ids.username.text
        password = self.ids.password.text

        if email == "" or password == "":
            self.show_popup("Login Gagal", "Email atau Password tidak boleh kosong!")
            return

        try:
            users = db.child("users").get()
            for user in users.each():
                user_data = user.val()
                if user_data['email'] == email and user_data['password'] == password:
                    username = user_data['username']
                    role = user_data['role']
                    user_id = user_data['uid']

                    self.current_user_uid = user_id

                    self.manager.get_screen('main').set_username(username)
                    self.manager.get_screen('user_absen').set_user_id(user_id)

                    if role == 'Admin':
                        self.manager.current = 'main'
                    else:
                        self.manager.current = 'user_absen'

                    self.show_popup("Login Berhasil", f"Selamat datang, {username}!")
                    return

            self.show_popup("Login Gagal", "Email atau Password salah.")

        except Exception as e:
            self.show_popup("Login Gagal", f"Terjadi kesalahan: {str(e)}")
            
    def go_to_resetpw(self):
        self.manager.current = 'resetpw'

    def go_to_signup(self):
        self.manager.current = 'signup'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()


class ProfileScreen(Screen):
    def on_enter(self):
        self.current_uid = self.manager.get_screen('login').current_user_uid
