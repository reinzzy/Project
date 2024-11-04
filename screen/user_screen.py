from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label

class UserScreen(Screen):
    def go_to_attendance(self):
        self.manager.current = 'attendance'

    def set_user_id(self, user_id):
        self.user_id = user_id

    def confirm_logout(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Apakah Anda yakin ingin logout?"))

        popup = Popup(title="Konfirmasi Logout", content=layout, size_hint=(0.6, 0.4))

        yes_button = Button(text="Ya", size_hint=(1, 0.5))
        yes_button.bind(on_release=lambda *args: self.logout(popup))  
        layout.add_widget(yes_button)

        no_button = Button(text="Tidak", size_hint=(1, 0.5))
        no_button.bind(on_release=popup.dismiss)  
        layout.add_widget(no_button)

        popup.open()

    def logout(self, popup):
        popup.dismiss()
        self.manager.current = 'login'
