import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/signup.kv')
Builder.load_file(kv_path)

class SignupScreen(Screen):
    def register(self):
        username = self.ids.signup_username.text
        password = self.ids.signup_password.text
        verify_password = self.ids.verify_password.text

        if password != verify_password:
            self.ids.signup_message.text = "Password tidak cocok!"
        elif username == "" or password == "":
            self.ids.signup_message.text = "Username atau Password tidak boleh kosong!"
        else:
            self.ids.signup_message.text = "Registrasi berhasil!"
            self.manager.current = 'login'