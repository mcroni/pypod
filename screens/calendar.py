from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from models_sql import *
from mat.list import OneLineListItem
import _thread
import time


class Calendar(Screen):
    ml = ObjectProperty(None)
    scroller = ObjectProperty(None)
    button = ObjectProperty(None)

    def _thread_announcement(self):
        print("checking Events")
        _thread.start_new_thread(self.load_announcements, ('bb',))

    def load_announcements(self, bb):
        self.ids.spinner.active = True
        time.sleep(2)
        for message in Announcementss.select():
            self.ids.ml.remove_widget(self.button)
            time.sleep(1)
            self.ids.ml.add_widget(OneLineListItem(text=str(message.message)))
            self.ids.spinner.active = False

