from kivy.properties import ObjectProperty
from mat.list import MDList
from mat.list import TwoLineListItem
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from models_sql import *
from mat.toast import Toast
from screens.testimonies import PopList
import time
import _thread
import peewee
import mat.snackbar as Snackbar


class Pastors(Screen, FloatLayout):
    pas_text_field = ObjectProperty(None)
    name_text_field = ObjectProperty(None)

    def login_thread(self):
        _thread.start_new_thread(self.login, ('dbb',))
    db = []

    def login(self,dbb):
        if len(self.name_text_field.text) ==0:
            self.login_failure('wrong credentials')
        if len(self.pas_text_field.text)== 0:
            self.login_failure('wrong credentials')
        else:
            try:
                for name in PastorsCircle.select():
                    if self.name_text_field.text == name.name and self.pas_text_field.text == name.password:
                        print("yes i dey")
                        self.name_text_field.text = ''
                        self.pas_text_field.text = ''
                        self.ids.spinner.active = False
                        App.get_running_app().root.next_screen('requests_reader')
            except peewee.OperationalError:
                self.ids.spinner.active = False
                self.ids.spinner.active = False
                self.ids.button.text='Try Again'
                self.name_text_field.text = ''
                self.pas_text_field.text = ''
                self.login_failure('check internet connection')

            else:
                pass

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)


class RequestsReader(Screen):
    def load_requests(self):
        content = ScrollView()
        mdlist = MDList()
        content.add_widget(mdlist)
        title = "Prayer Requests"
        pop = Popup(title=title,content=content)
        pop.open()
        try:
            for prayer in PrayerRequest.select():
                mdlist.add_widget(PopList(text=str(prayer.name), secondary_text=str(prayer.prayer_request)))
        except peewee.OperationalError:
            mdlist.add_widget(PopList(text=str('Error'), secondary_text=str('Please Check The Internet Connection and Try Again')))
        else:
            pass

    def add_announce(self):
        pop = Announce()
        pop.open()


class Announce(Popup):
    message = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Announce, self).__init__(**kwargs)

    def add_announce(self):
        if len(self.message.text) == 0:
            self.show_example_snackbar('simple')

        else:
            try:
                add_announce = Announcementss(message=self.ids.message.text)
                add_announce.save()
                print('added announcement')
                self.ids.message.text = ''
                self.dismiss()
                self.show_example_snackbar('sent')
            except peewee.OperationalError:
                self.show_example_snackbar('sent')
            else:
                pass


    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar.make("Please key in Something")
        if snack_type == 'try':
            Snackbar.make("Please Try Again")
        elif snack_type == 'sent':
            Snackbar.make("Announcement Sent")
