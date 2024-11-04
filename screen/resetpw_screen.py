import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty
from config import firebase_config
import random
import string

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

class ResetPasswordScreen(Screen):
    captcha_text = StringProperty()

    def __init__(self, **kwargs):
        super(ResetPasswordScreen, self).__init__(**kwargs)
        self.captcha_text = self.generate_captcha()  # Generate CAPTCHA

    def generate_captcha(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def reset_password(self, instance):
        email = self.ids.email_input.text
        new_password = self.ids.new_password_input.text
        input_captcha = self.ids.captcha_input.text

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
