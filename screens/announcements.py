from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from mat.list import OneLineListItem
from kivy.properties import ObjectProperty
from models_sql import *
import _thread
import time
import requests
import peewee
from mat.toast import Toast
from screens.testimonies import PopList

class Announcements(Screen,FloatLayout):
    ml = ObjectProperty(None)
    scroller = ObjectProperty(None)
    button = ObjectProperty(None)

    def _thread_announcement(self):
        print("loggin in")
        _thread.start_new_thread(self.load_announcements, ('bb',))

    def load_announcements(self,bb):
        self.ids.spinner.active = True
        try:
            for message in Announcementss.select():
                time.sleep(1)
                self.ids.spinner.active = False

                self.ids.ml.add_widget(PopList(text=str(message.message)))

        except peewee.OperationalError:
            print('cant connect')
            self.login_failure('cannot connect,try again')
            self.ids.spinner.active = False

        else:
            pass

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)
