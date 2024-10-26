from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
import os
from datetime import datetime
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

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/attendance.kv')
Builder.load_file(kv_path)

class AttendanceScreen(Screen):
    def on_enter(self):
        self.user_id = self.manager.get_screen('user_absen').user_id

    def submit_attendance(self):
        attendance_category = self.ids.attendance_spinner.text
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if attendance_category == "Pilih Kategori":
            self.show_popup("Absen Gagal", "Silakan pilih kategori absensi!")
            return

        attendance_data = {
            "user_id": self.user_id,
            "category": attendance_category,
            "timestamp": timestamp
        }

        try:
            db.child("attendance").push(attendance_data)
            self.show_popup("Absen Berhasil", f"Absensi '{attendance_category}' berhasil dicatat.")
            self.ids.attendance_spinner.text = "Pilih Kategori"
        except Exception as e:
            self.show_popup("Absen Gagal", f"Terjadi kesalahan: {str(e)}")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message)
        popup_layout.add_widget(popup_label)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        popup_layout.add_widget(ok_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
