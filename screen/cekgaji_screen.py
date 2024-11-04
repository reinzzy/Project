import os
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
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

        if not salaries.each():
            self.show_no_data_popup()  
            return

        data = []
        for salary in salaries.each():
            entry = salary.val()
            name = salary.key()
            amount = int(entry.get('amount', 0))
            allowance = int(entry.get('allowance', 0))
            bonus = int(entry.get('bonus', 0))

            formatted_amount = self.format_rupiah(amount)
            formatted_allowance = self.format_rupiah(allowance)
            formatted_bonus = self.format_rupiah(bonus)

            data.append((name, formatted_amount, formatted_allowance, formatted_bonus))

        self.display_table(data)

    def show_no_data_popup(self):
        dialog = MDDialog(
            title="Data Tidak Ditemukan",
            text="Tidak ada data gaji yang tersedia.",
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

    def format_rupiah(self, value):
        return f"Rp {value:,.0f}".replace(",", ".")

    def display_table(self, data):
        if hasattr(self, 'table'):
            self.ids.table_container.remove_widget(self.table)

        self.table = MDDataTable(
            size_hint=(1, 0.8),
            column_data=[
                ("Nama", dp(30)),
                ("Gaji Pokok", dp(30)),
                ("Tunjangan", dp(30)),
                ("Bonus", dp(30)),
            ],
            row_data=data,
        )
        
        self.ids.table_container.add_widget(self.table)

    def create_pdf(self, data, filename):
        pdf = canvas.Canvas(filename, pagesize=letter)
        pdf.setTitle("Rekap Gaji Karyawan")

        x = 50
        y = 750

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(x, y, "Rekap Gaji Karyawan")

        pdf.setFont("Helvetica", 12)
        y -= 30

        columns = ["Nama", "Gaji Pokok", "Tunjangan", "Bonus"]
        for col in columns:
            pdf.drawString(x, y, str(col))
            x += 100  

        x = 50
        y -= 20

        for entry in data:
            for item in entry:
                pdf.drawString(x, y, str(item))
                x += 100  
            x = 50  
            y -= 20  

        pdf.save() 

    def print_pdf(self):
        data = [(name, amount, allowance, bonus) for name, amount, allowance, bonus in self.table.row_data]
        self.create_pdf(data, "rekap_gaji_karyawan.pdf")
        print("PDF telah dibuat: rekap_gaji_karyawan.pdf")
