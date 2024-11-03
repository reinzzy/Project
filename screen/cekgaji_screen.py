import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivytable import KivyTable  # Pastikan KivyTable sudah diinstal

# Konfigurasi Firebase
firebase_config = {
    "apiKey": "AIzaSyCMDIZ_s0HG3Ozh_1tccSCaWmXC-0kZo1Y",
    "authDomain": "projectpython-58225.firebaseapp.com",
    "databaseURL": "https://projectpython-58225-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "projectpython-58225",
    "storageBucket": "projectpython-58225.appspot.com",
    "messagingSenderId": "635697293104",
    "appId": "1:635697293104:android:afe47f84df46cc64020af5"
}

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Load file KV
kv_path = os.path.join(os.path.dirname(__file__), '../kivy/cekgaji.kv')
Builder.load_file(kv_path)

class CekGaji(Screen):
    def on_enter(self):
        self.fetch_salaries()  # Ambil data saat layar dimasuki

    def fetch_salaries(self):
        # Ambil data dari koleksi salaries di Realtime Database
        salaries = db.child("salaries").get()  # Ganti dengan nama koleksi Anda

        # Buat list untuk menyimpan data gaji
        data = []
        for salary in salaries.each():
            data.append(salary.val())  # Mengonversi setiap item menjadi dictionary

        # Tampilkan data di KivyTable
        self.display_table(data)

    def display_table(self, data):
        # Konfigurasi KivyTable
        if hasattr(self, 'table'):  # Cek apakah tabel sudah ada
            self.ids.table_container.remove_widget(self.table)  # Hapus tabel lama

        self.table = KivyTable()  # Membuat instance KivyTable
        self.table.column_names = ['Nama', 'Gaji', 'Tanggal']  # Ganti sesuai dengan field di Firebase

        # Menambahkan data ke tabel
        for entry in data:
            self.table.add_row([entry.get('name'), entry.get('salary'), entry.get('date')])  # Ganti dengan field yang sesuai

        self.ids.table_container.add_widget(self.table)  # Tambahkan tabel ke container di layout
