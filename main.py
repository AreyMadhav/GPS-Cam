import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import camera, gps, permission
from kivy.utils import platform

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Label to display the message
        self.message_label = Label(text="Press the button below")
        self.layout.add_widget(self.message_label)

        # Button to take a picture
        self.camera_button = Button(text="Take Picture")
        self.camera_button.bind(on_press=self.request_camera_permission)
        self.layout.add_widget(self.camera_button)

        # Button to get GPS location
        self.gps_button = Button(text="Get GPS Location")
        self.gps_button.bind(on_press=self.request_gps_permission)
        self.layout.add_widget(self.gps_button)

        # Label to display GPS location
        self.gps_label = Label(text="GPS Location: Waiting for location...")
        self.layout.add_widget(self.gps_label)

        return self.layout

    def request_camera_permission(self, instance):
        permission.request_permissions([permission.PERMISSION_CAMERA], self.take_picture)

    def request_gps_permission(self, instance):
        permission.request_permissions([permission.PERMISSION_LOCATION], self.get_location)

    def take_picture(self, *args):
        # Save the image to the internal storage path
        path = os.path.join(self.get_app_storage_path(), "my_picture.jpg")
        camera.take_picture(filename=path, on_complete=self.picture_taken)

    def get_app_storage_path(self):
        return os.path.expanduser("~")

    def picture_taken(self, path):
        self.message_label.text = f"Picture saved at {path}"

    def get_location(self):
        gps.configure(on_location=self.update_gps_location, on_status=self.update_gps_status)
        gps.start()

    def update_gps_location(self, **kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        self.gps_label.text = f"GPS Location: Latitude: {lat}, Longitude: {lon}"

    def update_gps_status(self, status):
        self.gps_label.text = f"GPS Status: {status}"

if __name__ == '__main__':
    MyApp().run()
