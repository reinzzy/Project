import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget

kv_path = os.path.join(os.path.dirname(__file__), '../kivy/absensi.kv')
Builder.load_file(kv_path)

# Define the details screen here for simplicity
class EmployeeDetailsScreen(Screen):
    pass

class AbsensiScreen(Screen):
    def on_pre_enter(self):
        # Sample data for employees
        employees = [
            {"name": "Dendi", "attendance": "✔ ✔ ✔", "details": "Sakit: 3x, Ijin: 1x"},
            {"name": "Rival", "attendance": "✘ ✔ ✔", "details": "Sakit: 2x, Ijin: 0x"},
            {"name": "Rezaldi", "attendance": "✔ ✔ ✔", "details": "Sakit: 2x, Ijin: 0x"},
            {"name": "Zaki", "attendance": "✔ ✔ ✘", "details": "Sakit: 4x, Ijin: 0x"},
        ]
        
        # Clear the list to prevent duplicate entries
        self.ids.employee_list.clear_widgets()
        
        for employee in employees:
            # Create a new list item for each employee
            item = OneLineAvatarIconListItem(text=employee["name"])
            button = IconRightWidget(icon="open-in-new")
            button.bind(on_release=lambda instance, emp=employee: self.open_details(emp))
            item.add_widget(button)
            self.ids.employee_list.add_widget(item)

    def open_details(self, employee):
        # Set the details screen content based on the employee data
        details_screen = self.manager.get_screen("employee_details")
        details_screen.ids.employee_name.text = f"Name: {employee['name']}\nDetails: {employee['details']}"
        self.manager.current = "employee_details"
