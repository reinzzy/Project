import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/cekgaji.kv')
Builder.load_file(kv_path)

class CekGaji(Screen):
    def on_enter(self):
        self.fetch_salaries() 

    def fetch_salaries(self):
        salaries = db.child("salaries").get() 

        data = []
        for salary in salaries.each():
            entry = salary.val()
            name = salary.key()
            allowance = int(entry.get('allowance', 0))
            amount = int(entry.get('amount', 0))
            bonus = int(entry.get('bonus', 0))

            formatted_allowance = self.format_rupiah(allowance)
            formatted_amount = self.format_rupiah(amount)
            formatted_bonus = self.format_rupiah(bonus)

            data.append((name, formatted_allowance, formatted_amount, formatted_bonus))

        self.display_table(data)

    def format_rupiah(self, value):
        return f"Rp {value:,.0f}".replace(",", ".")

    def display_table(self, data):
        if hasattr(self, 'table'):
            self.ids.table_container.remove_widget(self.table)

        self.table = MDDataTable(
            size_hint=(1, 0.8),
            column_data=[
                ("Nama", dp(30)),
                ("Tunjangan", dp(30)),
                ("Gaji Pokok", dp(30)),
                ("Bonus", dp(30)),
            ],
            row_data=data,
        )
        
        self.ids.table_container.add_widget(self.table)
