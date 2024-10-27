import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget, MDList
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
import pyrebase
from datetime import datetime

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

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/absensi.kv')
Builder.load_file(kv_path)

class AbsensiScreen(Screen):
    def on_pre_enter(self):
        # Panggil fetch_attendance_data setiap kali layar ditampilkan
        self.fetch_attendance_data()

    def fetch_attendance_data(self):
        try:
            # Clear the list to prevent duplicate entries
            self.ids.employee_list.clear_widgets()

            # Retrieve attendance data from Firebase
            attendance_data = db.child("attendance").get().val()
            if attendance_data:
                grouped_data = {}  # Dictionary to hold attendance grouped by username

                # Group attendance records by username
                for record_id, record in attendance_data.items():
                    user_id = record.get("user_id")
                    category = record.get("category")
                    timestamp = record.get("timestamp")
                    date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y %H:%M') if timestamp else "Unknown"

                    # Get the username from the user_id
                    user_data = db.child("users").child(user_id).get().val()
                    username = user_data.get("username") if user_data else "Unknown User"

                    # Group attendance records by username
                    if username not in grouped_data:
                        grouped_data[username] = []
                    grouped_data[username].append(f"{category} - {date_time}")

                # Create a spinner for each user with their attendance records
                for username, records in grouped_data.items():
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height=40)
                    spinner = Spinner(
                        text=username,
                        values=records,
                        size_hint=(1, None),
                        height=40
                    )
                    box.add_widget(spinner)
                    self.ids.employee_list.add_widget(box)

            else:
                print("Tidak ada data absensi.")

        except Exception as e:
            print(f"Error saat mengambil data dari Firebase: {e}")

    def go_back(self):
        self.manager.current = "main"
