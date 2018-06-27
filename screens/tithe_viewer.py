from kivy.uix.screenmanager import Screen
from persons import Tithe as Tither
from mat.list import TwoLineListItem
from kivy.app import App
from kivy.properties import ObjectProperty


class TitheViewer(Screen):
    ml = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TitheViewer, self).__init__(**kwargs)

    def adder(self):
        self.ml.clear_widgets()
        for tithes in Tither.select():
            self.ml.add_widget(TwoLineListItem(text=str(tithes.month),
                                                   secondary_text=str(tithes.amount)))
