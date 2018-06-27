from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from models_sql import *
import _thread
from mat.list import OneLineAvatarListItem
from kivy.metrics import dp
from mat.toast import Toast
from kivy.uix.image import AsyncImage
from mat.list import ILeftBody
import peewee
from mat.dialog import MDDialog
from mat.label import MDLabel


class Quotes(Screen,FloatLayout):
    ml = ObjectProperty(None)
    scroller = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Quotes,self).__init__(**kwargs)

    def thread_announcement(self):
        print("loggin in")
        _thread.start_new_thread(self.load_announcements, ('bb',))

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def load_announcements(self, bb):
        try:
            self.ids.spinner.active = True
            for quotes in Quotations.select():
                self.but = QuoteButton(text=str(quotes.name))
                self.but.add_widget(Photo(source='tower.png'))
                self.ids.ml.add_widget(self.but)
            self.ids.spinner.active = False
            self.login_failure('Double Tap on A Quote\nto Share')
        except peewee.OperationalError:
            self.ids.spinner.active = False
            self.login_failure('Check Internet Connection')
        else:
            pass


class Photo(ILeftBody, AsyncImage):
    pass

    # def share(self):
    #     intent = Intent()
    #     intent.setAction(Intent.ACTION_SEND)
    #     intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(self.source)))
    #     intent.setType('text/plain')
    #     chooser = Intent.createChooser(intent, String('Share...'))
    #     PythonActivity.mActivity.startActivity(chooser)


class QuoteButton(OneLineAvatarListItem):
    def __init__(self,**kwargs):
        super(QuoteButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            if touch.is_double_tap:
                print('doouble')
            else:
                content = MDLabel(font_style='Body1',
                                  theme_text_color='Secondary',
                                  text="{}".format(self.secondary_text),
                                  valign='top')

                content.bind(size=content.setter('text_size'))
                self.dialog = MDDialog(title="{}".format(self.text), content=content, size_hint=(.9, None),
                                       height=dp(200), auto_dismiss=False)

                self.dialog.add_action_button("Dismiss",
                                              action=lambda *x: self.dialog.dismiss())
                self.dialog.open()
        super(QuoteButton, self).on_touch_down(touch)