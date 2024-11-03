import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import pyrebase

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
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/addgaji.kv')
Builder.load_file(kv_path)

class AddGaji(Screen):
    def on_enter(self):
        self.ids.user_spinner.values = self.get_users_with_role("User")

    def get_users_with_role(self, role):
        try:
            users = db.child("users").get().val()
            if users:
                return [user['username'] for user in users.values() if user.get('role') == role]
            return []
        except Exception as e:
            print(f"Error saat mengambil data user: {e}")
            return []

    def on_user_select(self, selected_user):
        user_id = self.get_user_id(selected_user)
        attendance_count = self.get_attendance_count(user_id)
        self.ids.attendance_input.text = str(attendance_count)
        self.ids.attendance_input.disabled = True

    def add_salary(self):
        selected_user = self.ids.user_spinner.text
        salary_per_presence = 80000
        
        if selected_user:
            attendance_count = int(self.ids.attendance_input.text)
            allowance = int(self.ids.allowance_input.text)
            bonus = int(self.ids.bonus_input.text)

            total_salary = (attendance_count * salary_per_presence) + allowance + bonus

            db.child("salaries").child(selected_user).update({
                "amount": total_salary,
                "allowance": allowance,
                "bonus": bonus
            })
            self.show_success_dialog()
        else:
            print("User tidak dipilih!")

    def get_user_id(self, username):
        try:
            users = db.child("users").get().val()
            if users:
                for user in users.values():
                    if user.get('username') == username:
                        return user.get('uid')
        except Exception as e:
            print(f"Error saat mengambil user_id: {e}")
        return None

    def get_attendance_count(self, user_id):
        try:
            attendance_data = db.child("attendance").get().val()
            count = 0
            if attendance_data:
                for record in attendance_data.values():
                    if record.get('user_id') == user_id and record.get('category') == 'Masuk':
                        count += 1
            return count
        except Exception as e:
            print(f"Error saat menghitung kehadiran: {e}")
            return 0

    def show_success_dialog(self):
        dialog = MDDialog(
            title="Sukses",
            text="Gaji berhasil ditambahkan!",
            size_hint=(0.8, None),
            height=dp(200),
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()