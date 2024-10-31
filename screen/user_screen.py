from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
import os

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/user.kv')
Builder.load_file(kv_path)

class UserScreen(Screen):
    def go_to_attendance(self):
        self.manager.current = 'attendance'

    def set_user_id(self, user_id):
        self.user_id = user_id

    def confirm_logout(self):
        # Membuat layout popup konfirmasi
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Apakah Anda yakin ingin logout?"))

        # Membuat popup
        popup = Popup(title="Konfirmasi Logout", content=layout, size_hint=(0.6, 0.4))

        # Tombol "Ya" untuk konfirmasi logout
        yes_button = Button(text="Ya", size_hint=(1, 0.5))
        yes_button.bind(on_release=lambda *args: self.logout(popup))  # Menutup popup di logout
        layout.add_widget(yes_button)

        # Tombol "Tidak" untuk membatalkan logout
        no_button = Button(text="Tidak", size_hint=(1, 0.5))
        no_button.bind(on_release=popup.dismiss)  # Menutup popup saat memilih "Tidak"
        layout.add_widget(no_button)

        # Membuka popup
        popup.open()

    def logout(self, popup):
        # Fungsi logout
        popup.dismiss()  # Menutup popup
        self.manager.current = 'login'
