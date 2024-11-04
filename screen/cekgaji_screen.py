from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import pyrebase
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

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
        width, height = letter
        
        # Header 
        pdf.setFillColor(colors.HexColor("#2C3E50"))
        pdf.rect(0, height - 80, width, 80, fill=True, stroke=False)
        
        pdf.setFont("Helvetica-Bold", 20)
        pdf.setFillColor(colors.white)
        pdf.drawString(50, height - 50, "Rekap Gaji Karyawan")
        
        # Footer 
        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.HexColor("#7F8C8D"))
        pdf.drawString(50, 30, "Rekap Gaji Karyawan © 2024")

        # Judul Kolom
        columns = ["Nama", "Gaji Pokok", "Tunjangan", "Bonus"]
        column_width = (width - 100) / len(columns)
        
        pdf.setFillColor(colors.HexColor("#34495E"))
        pdf.setFont("Helvetica-Bold", 12)
        y = height - 130
        for i, col in enumerate(columns):
            pdf.drawString(50 + i * column_width, y, col)

        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.black)
        y -= 15
        for entry in data:
            for i, item in enumerate(entry):
                pdf.drawString(50 + i * column_width, y, str(item))
            y -= 20
            pdf.setStrokeColor(colors.HexColor("#BDC3C7"))
            pdf.setLineWidth(0.5)
            pdf.line(50, y + 10, width - 50, y + 10)

        pdf.save()

    def print_pdf(self):
        data = [(name, amount, allowance, bonus) for name, amount, allowance, bonus in self.table.row_data]
        self.create_pdf(data, "rekap_gaji_karyawan.pdf")
