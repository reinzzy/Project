from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
import pyrebase
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

class AbsensiScreen(Screen):
    def on_enter(self):
        self.fetch_attendance_data()

    def fetch_attendance_data(self):
        try:
            self.ids.employee_list.clear_widgets()
            attendance_data = db.child("attendance").get().val()

            if attendance_data:
                grouped_data = self.group_attendance_data(attendance_data)
                self.display_attendance_data(grouped_data)
            else:
                print("Tidak ada data absensi.")
        except Exception as e:
            print(f"Error saat mengambil data dari Firebase: {e}")

    def group_attendance_data(self, attendance_data):
        grouped_data = {}
        for record_id, record in attendance_data.items():
            user_id = record.get("user_id")
            category = record.get("category")

            user_data = db.child("users").child(user_id).get().val()
            if user_data:
                username = user_data.get("username")
                if username not in grouped_data:
                    grouped_data[username] = {"Masuk": 0, "Izin": 0, "Sakit": 0}

                if category in grouped_data[username]:
                    grouped_data[username][category] += 1
                else:
                    print(f"Kategori tidak dikenali: {category}")
            else:
                print(f"User data not found for User ID: {user_id}")

        return grouped_data

    def display_attendance_data(self, grouped_data):
        columns = [
            ("Nama", 30),
            ("Masuk", 20),
            ("Izin", 20),
            ("Sakit", 20),
        ]

        row_data = []
        for username, counts in grouped_data.items():
            masuk_count = str(counts.get("Masuk", 0))
            izin_count = str(counts.get("Izin", 0))
            sakit_count = str(counts.get("Sakit", 0))
            row_data.append([username, masuk_count, izin_count, sakit_count])

        self.data_table = MDDataTable(
            size_hint=(1, None),
            height=self.height - 200,
            column_data=columns,
            row_data=row_data,
            elevation=2,
            use_pagination=True,
        )

        self.ids.employee_list.add_widget(self.data_table)

    def go_back(self):
        self.manager.current = "main"
