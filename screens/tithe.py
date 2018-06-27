from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from persons import Tithe as Tt
from kivy.properties import ObjectProperty
from mat.toast import Toast
from kivy.uix.floatlayout import FloatLayout


class Tithe(Screen):
    grid = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Tithe,self).__init__(**kwargs)

    def adder(self):
        months_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for month in months_list:
            self.grid.add_widget(TitheButton(text=month,
                                                   on_pressed= lambda x: self.add_tithe()))

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def login_failure(self, error):
        self._show_toast(error)

    def toast(self):
        self.login_failure('type an amount')


class TitheButton(Button):
    def __init__(self,**kwargs):
        super(TitheButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print('touched',self.text)
            self.add_tithe()
        return super(TitheButton, self).on_touch_down(touch)

    def add_tithe(self):
        p = TithePopup()
        p.title= self.text
        p.open()


class TithePopup(Popup):
    amount = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(TithePopup,self).__init__(**kwargs)

    def on_add(self):
        print('called me',self.title)
        kudi = self.amount.text
        try:
            tithe_to_pay = ((10 / 100) * float(kudi))
            cr = ("%.02f" % tithe_to_pay)
            print(cr)
            month = Tt.get(Tt.month == self.title)
            old_amount = month.amount
            print(old_amount)
            new_amount = float(cr) + float(old_amount)
            print(new_amount)
            month.amount = new_amount
            month.save()
            self.dismiss()

        except ValueError:
            print('enter a figure')
            self.amount.text = ''
            self.amount.hint_text='sorry,enter an amount'
        else:
            pass

