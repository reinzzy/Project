import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty
from config import firebase_config
import pyrebase

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()
db = firebase.database()

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/profile.kv')
Builder.load_file(kv_path)

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.current_uid = None

    def on_enter(self):
        self.current_uid = self.manager.get_screen('login').current_user_uid
        self.load_profile()

    def load_profile(self):
        self.ids.name_input.text = ""
        self.ids.birth_date_input.text = ""
        self.ids.address_input.text = ""
        self.ids.email_input.text = ""
        self.ids.profile_image.source = 'asset/profile_icon.png'

        if not self.current_uid:
            print("UID pengguna tidak ditemukan.")
            return

        try:
            profile_data = db.child("profiles").child(self.current_uid).get()
            if profile_data.val():
                profile_info = profile_data.val()
                self.ids.name_input.text = profile_info.get("name", "")
                self.ids.birth_date_input.text = profile_info.get("birth_date", "")
                self.ids.address_input.text = profile_info.get("address", "")
                self.ids.email_input.text = profile_info.get("email", "")
                self.ids.profile_image.source = profile_info.get("profile_image", 'asset/profile_icon.png')
                print("Data profil berhasil dimuat!")
            else:
                print("Tidak ada data profil ditemukan untuk UID ini.")
        except Exception as e:
            print(f"Error memuat data profil: {e}")

    def open_filechooser(self):
        content = FileChooserPopup(select=self.upload_photo)
        content.open()

    def upload_photo(self, file_path):
        if not self.current_uid:
            print("UID pengguna tidak ditemukan.")
            return

        try:
            file_name = os.path.basename(file_path)
            storage.child("profile_photos/" + file_name).put(file_path)
            download_url = storage.child("profile_photos/" + file_name).get_url(None)
            self.ids.profile_image.source = download_url
            db.child("profiles").child(self.current_uid).update({"profile_image": download_url})
            print("Foto profil berhasil diunggah dan disimpan di database!")
        except Exception as e:
            print(f"Error mengunggah foto profil: {e}")

    def save_profile(self):
        if not self.current_uid:
            print("UID pengguna tidak ditemukan.")
            return

        name = self.ids.name_input.text
        birth_date = self.ids.birth_date_input.text
        address = self.ids.address_input.text
        email = self.ids.email_input.text
        profile_data = {
            "name": name,
            "birth_date": birth_date,
            "address": address,
            "email": email,
        }

        try:
            db.child("profiles").child(self.current_uid).set(profile_data)
            print("Data profil berhasil disimpan!")
        except Exception as e:
            print(f"Error menyimpan data profil: {e}")

    def show_logout_confirmation(self):
        popup = LogoutPopup(on_confirm=self.logout)
        popup.open()

    def logout(self):
        print("User telah logout")
        self.manager.current = 'login'

class FileChooserPopup(Popup):
    def __init__(self, select, **kwargs):
        super(FileChooserPopup, self).__init__(**kwargs)
        self.select = select
        self.selected_file = None
        self.title = "Pilih Foto"
        self.size_hint = (0.9, 0.9)

        self.filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        self.filechooser.bind(on_selection=self.on_select)
        
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.filechooser)

        select_btn = Button(text="Pilih Gambar", size_hint_y=None, height=40)
        select_btn.bind(on_release=lambda x: self.confirm_selection())
        layout.add_widget(select_btn)
        
        self.content = layout

    def on_select(self, *args):
        if args and args[1]:
            self.selected_file = args[1][0]
            print(f"File yang dipilih: {self.selected_file}")
        else:
            print("Tidak ada file yang dipilih dalam on_select.")

    def confirm_selection(self):
        if self.selected_file:
            self.select(self.selected_file)
            self.dismiss()
        else:
            print("Tidak ada file yang dipilih.")

class LogoutPopup(Popup):
    def __init__(self, on_confirm, **kwargs):
        super(LogoutPopup, self).__init__(**kwargs)
        self.on_confirm_action = on_confirm
        self.content = BoxLayout(orientation='vertical')
        self.content.add_widget(Label(text="Apakah Anda yakin ingin logout?"))
        self.content.add_widget(Button(text="Ya", on_release=self.on_confirm))
        self.content.add_widget(Button(text="Tidak", on_release=self.dismiss))

    def on_confirm(self, instance):
        self.dismiss()
        self.on_confirm_action()
