from kivy.uix.screenmanager import Screen
from mat.list import TwoLineListItem
import mat.snackbar as Snackbar
# from models_sql import Person
from plyer import call
from plyer import vibrator
import _thread
import peewee
from mat.toast import Toast

class Search(Screen):
    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)

    lists_of_names = []

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def loader(self):
        _thread.start_new_thread(self.load, ('name',))
        self.ids.search_input.bind(text=self.some_func)

    def load(self,name):
        try:
            for name in Person.select():
                self.ids.ml.add_widget(CallerButton(text=name.name, secondary_text=str(name.number)))
                contact = []
                contact.append(name.name)
                contact.append(name.number)
                self.lists_of_names.append(contact)
            print(self.lists_of_names)
        except peewee.OperationalError:
            self.login_failure('Please Try Again\nNo Connection')

    tem = '0'

    def some_func(self, *args):
        returned_name = self.ids.search_input.text
        print(returned_name)
        self.ids.ml.clear_widgets()
        for name in self.lists_of_names:
            if name[0].startswith(returned_name):
                print('yea')
                numm = self.tem + str(name[1])
                print(numm)
                self.ids.ml.add_widget(CallerButton(text=str(name[0]),secondary_text=numm))

        if len(self.ids.ml.children) == 0:
            self.show_example_snackbar('simple')

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar.make("Person Not Found :-( :-(", duration=2)
        if snack_type == 'fail':
            Snackbar.make("Please Check Internet Connection :-(", duration=2)


class CallerButton(TwoLineListItem):
    def __init__(self,**kwargs):
        super(CallerButton,self).__init__(**kwargs)

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            number =self.secondary_text
            print(number)
            tel = number
            vibrator.vibrate(.3)
            call.makecall(tel=tel)
            return True
        return super(CallerButton, self).on_touch_down(touch)

