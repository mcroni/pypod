from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from models_sql import *
import _thread
import peewee
from screens.testimonies import PopList

class Guide(Screen):
    ml = ObjectProperty(None)
    scroller = ObjectProperty(None)
    button = ObjectProperty(None)

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def thread_guide(self):
        _thread.start_new_thread(self.load_guides, ('dbb',))

    def load_guides(self, dbb):
        self.ids.ml.clear_widgets()
        try:
            self.ids.spinner.active = True
            for guide in DailyGuide.select():
                self.ids.ml.add_widget(PopList(text=guide.title, secondary_text=guide.message))
                self.ids.spinner.active = False
        except peewee.OperationalError:
            self.ids.spinner.active = True
            self.ids.ml.add_widget(PopList(text='error', secondary_text='please check your internet connection'))
        else:
            pass

