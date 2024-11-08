import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()  
db = firebase.database()

class SignupScreen(Screen):
    def register(self):
        username = self.ids.signup_username.text
        email = self.ids.signup_email.text
        password = self.ids.signup_password.text
        verify_password = self.ids.verify_password.text
        role = "User"

        if password != verify_password:
            self.ids.signup_message.text = "Password tidak cocok!"
        elif username == "" or email == "" or password == "":
            self.ids.signup_message.text = "Semua kolom harus diisi!"
        else:
            try:
                user = auth.create_user_with_email_and_password(email, password)

                user_data = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "uid": user["localId"],
                    "role": role
                }

                db.child("users").child(user["localId"]).set(user_data)

                self.ids.signup_message.text = "Registrasi berhasil!"
                self.manager.current = 'login'

            except Exception as e:
                print("Error during registration: ", e)

                error_message = str(e)
                if "EMAIL_EXISTS" in error_message:
                    self.ids.signup_message.text = "Email sudah terdaftar."
                elif "INVALID_EMAIL" in error_message:
                    self.ids.signup_message.text = "Format email tidak valid."
                elif "WEAK_PASSWORD" in error_message:
                    self.ids.signup_message.text = "Password terlalu lemah. Minimal 6 karakter."
                else:
                    self.ids.signup_message.text = f"Error: {error_message}"
