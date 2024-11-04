from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
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
        for username, counts in grouped_data.items():
            item = OneLineAvatarIconListItem(text=username)
            icon = IconRightWidget(icon="information")
            icon.bind(on_release=lambda instance, counts=counts, username=username: self.show_popup(username, counts))
            item.add_widget(icon)
            self.ids.employee_list.add_widget(item)

    def show_popup(self, username, counts):
        content = BoxLayout(orientation='vertical')
        masuk_count = counts.get("Masuk", 0)
        izin_count = counts.get("Izin", 0)
        sakit_count = counts.get("Sakit", 0)

        content.add_widget(Label(text=f"Masuk: {masuk_count}"))
        content.add_widget(Label(text=f"Izin: {izin_count}"))
        content.add_widget(Label(text=f"Sakit: {sakit_count}"))

        popup = Popup(title=f"Rekap Absensi - {username}", content=content, size_hint=(0.8, 0.4))
        popup.open()

    def go_back(self):
        self.manager.current = "main"
