import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty
import random
import string

firebase_config = {
    "apiKey": "AIzaSyCMDIZ_s0HG3Ozh_1tccSCaWmXC-0kZo1Y",
    "authDomain": "projectpython-58225.firebaseapp.com",
    "databaseURL": "https://projectpython-58225-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "projectpython-58225",
    "storageBucket": "projectpython-58225.appspot.com",
    "messagingSenderId": "635697293104",
    "appId": "1:635697293104:android:afe47f84df46cc64020af5"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/resetpw.kv')
Builder.load_file(kv_path)

class ResetPasswordScreen(Screen):
    captcha_text = StringProperty()

    def __init__(self, **kwargs):
        super(ResetPasswordScreen, self).__init__(**kwargs)
        self.captcha_text = self.generate_captcha()  # Generate CAPTCHA

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.email_input = TextInput(hint_text="Masukkan email Anda", multiline=False)
        layout.add_widget(self.email_input)

        self.new_password_input = TextInput(hint_text="Masukkan password baru", password=True, multiline=False)
        layout.add_widget(self.new_password_input)

        self.captcha_label = Label(text=self.captcha_text, font_size='20sp', bold=True)
        layout.add_widget(self.captcha_label)

        self.captcha_input = TextInput(hint_text="Masukkan teks captcha", multiline=False)
        layout.add_widget(self.captcha_input)

        reset_button = Button(text="Ganti Password")
        reset_button.bind(on_press=self.reset_password)
        layout.add_widget(reset_button)

        self.add_widget(layout)

    def generate_captcha(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def reset_password(self, instance):
        email = self.email_input.text
        new_password = self.new_password_input.text
        input_captcha = self.captcha_input.text

        if email == "" or new_password == "" or input_captcha == "":
            self.show_popup("Error", "Email, password, dan captcha tidak boleh kosong!")
            return

        if input_captcha != self.captcha_text:
            self.show_popup("Error", "Captcha salah. Silakan coba lagi.")
            self.captcha_text = self.generate_captcha()
            return

        try:
            users = db.child("users").get()
            user_found = False

            for user in users.each():
                if user.val().get("email") == email:
                    user_found = True
                    user_id = user.key()

                    db.child("users").child(user_id).update({"password": new_password})
                    self.show_popup("Sukses", "Password berhasil diganti!")
                    self.manager.current = 'login'
                    break
            
            if not user_found:
                self.show_popup("Error", "Email tidak terdaftar.")

        except Exception as e:
            self.show_popup("Error", f"Terjadi kesalahan: {str(e)}")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
