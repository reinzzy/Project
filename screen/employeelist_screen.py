import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import pyrebase
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/employeelist.kv')
Builder.load_file(kv_path)

class EmployeeListScreen(Screen):
    def on_enter(self):
        self.load_employee_data()

    def load_employee_data(self):
        # Kosongkan tampilan daftar karyawan
        employee_list = self.ids.employee_list
        employee_list.clear_widgets()

        try:
            users = db.child("users").get()
            # Menambahkan pengguna berperan 'user' ke daftar
            for idx, user in enumerate(users.each(), start=1):
                user_data = user.val()
                if user_data.get('role') == 'User':
                    employee_info = Label(
                        text=f"{idx}. {user_data.get('username')} - {user_data.get('email')}",
                        size_hint_y=None,
                        height=50,
                        color=[1, 1, 1, 1],  # Warna putih
                        font_size=18,
                        halign='left'
                    )
                    employee_list.add_widget(employee_info)

        except Exception as e:
            print(f"Error saat mengambil data dari Firebase: {e}")

    def go_back(self):
        self.manager.current = 'main'