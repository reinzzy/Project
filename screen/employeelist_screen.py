from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
import pyrebase
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

class EmployeeListScreen(Screen):
    def on_enter(self):
        self.load_employee_data()

    def load_employee_data(self):
        employee_list = self.ids.employee_list
        employee_list.clear_widgets()

        try:
            users = db.child("users").get()
            # Menyusun kolom untuk DataTable
            columns = [
                ("No", 10),
                ("Nama", 30),
                ("Email", 60),
            ]

            # Menyusun data untuk baris
            row_data = []

            # Cek apakah data ada
            if not users:
                print("Tidak ada data pengguna di Firebase.")
                return

            # Mengambil data pengguna dengan role 'User'
            for idx, user in enumerate(users.each(), start=1):
                user_data = user.val()

                # Filter berdasarkan role 'User'
                if user_data.get('role') == 'User':
                    username = user_data.get('username', 'N/A')
                    email = user_data.get('email', 'N/A')

                    # Menambahkan data ke row_data
                    row_data.append([str(idx), username, email])

            # Pastikan ada data untuk ditampilkan
            if not row_data:
                print("Tidak ada karyawan dengan role 'User'.")
                return

            # Membuat MDDataTable
            data_table = MDDataTable(
                size_hint=(1, None),
                height=self.height - 100,  # Menyesuaikan tinggi tabel
                column_data=columns,
                row_data=row_data,
                elevation=2,
                use_pagination=True,
            )

            # Menambahkan MDDataTable ke dalam layout
            employee_list.add_widget(data_table)

        except Exception as e:
            print(f"Error saat mengambil data dari Firebase: {e}")

    def go_back(self):
        self.manager.current = 'main'
