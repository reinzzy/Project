import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
import pyrebase
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

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
            allowance = int(self.ids.allowance_input.text) if self.ids.allowance_input.text else 0  
            bonus = int(self.ids.bonus_input.text) if self.ids.bonus_input.text else 0  

            total_salary = (attendance_count * salary_per_presence)

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
            print(f"Kehadiran untuk user_id {user_id}: {count}")  # Tambahkan ini
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
