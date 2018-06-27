# from kivy.uix.popup import Popup
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
# from kivymd.list import MDList
from kivy.properties import ObjectProperty
# from kivymd.list import TwoLineListItem
# from models_sql import *
import threading
import time
# from kivymd.dialog import MDDialog
# from kivymd.label import MDLabel
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
import kivymd.snackbar as Snackbar
from kivy.app import App
import feedparser
from kivy.clock import Clock
from main import PodList,AvatarSampleWidget,IconRightSampleWidget,ContactPhoto
from kivy.storage.jsonstore import JsonStore
store = JsonStore('python_bytes.json')

class PythonBytesScreen(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(PythonBytesScreen, self).__init__(**kwargs)
        self.refresher = False
        self.loaded = False

    def load_thread(self):
        print("calling the thread")
        t = threading.Thread(target=self.loader,args=("i",))
        t.start()

    def loader(self,args):
        print("loading in thread")
        self.ids.spinner.active = True
        url = "https://pythonbytes.fm/episodes/rss"
        try:
            data = feedparser.parse(url)
            print(data['feed']['title'])
            if data['feed']['title'] == "Python Bytes":
                print("grabbed data successfully")
                print(len(data['entries']))
                for i in data['entries']:
                    print(i.keys())
                    print(i['title'])
                    print(i['links'][1]['href'])
                    pod = PodList(text=i['title'][:25] + "...")
                    pod.data = i
                    store.put("{0}".format(i['title']),info=i)
                    avatar_widget = AvatarSampleWidget(source = './assets/python_bytes.png')
                    icon_right_widget = IconRightSampleWidget(icon="playlist-plus")
                    icon_right_widget.parent_title = i['title']
                    icon_right_widget.provider = 'python_bytes'
                    icon_right_widget.liked = False
                    pod.add_widget(avatar_widget)
                    pod.add_widget(icon_right_widget)
                    self.ids.ml.add_widget(pod)
                    time.sleep(0.09)
                self.ids.spinner.active = False

        except Exception as e:
            print(e)
            self.ids.spinner.active = False

    def load_rss(self):
        print(len(store.keys()))
        if len(store.keys()) != 0:
            print("things dey")
            for i in store.keys():
                print(i,store.get(i))
                data = store.get(i)['info']
                title = data['title']
                pod = PodList(text=title[:25] + "...")
                pod.data = data
                avatar_widget = AvatarSampleWidget(source='./assets/python_bytes.png')
                icon_right_widget = IconRightSampleWidget(icon="playlist-plus")
                icon_right_widget.parent_title = title
                icon_right_widget.provider = 'python_bytes'
                icon_right_widget.liked = False
                pod.add_widget(avatar_widget)
                pod.add_widget(icon_right_widget)
                self.ids.ml.add_widget(pod)
        else:
            print("fresh")
            if not self.loaded:
                print("loading rss feeds for this podcast")
                self.load_thread()
                self.loaded = True
            else:
                print("already loaded for this screen")

        # self.ids.toolbar.title = "python bytes"
        # App.get_running_app().theme_cls.primary_palette='Yellow'
        # self.ids.loader

    def move(self,pod_item):
        print(self.ids.pod_item.touch.pos)
        print("moving",self)

    def add_to_fav(self):
        print("adding to fav")

    def return_toolbar(self):
        pass
        # anim = Animation(pos_hint={'top': 1}, duration=2, t='in_back')
        # anim.start(self.ids.toolbar_box)
        # anim = Animation(top=0)
        # anim.start(self.ids.toolbar_box)

    def refresh(self):
        # anim = Animation(y=0)
        # anim.start(self.ids.toolbar_box)
        # anim = Animation(pos=(0, 10))
        # anim.start(self.ids.toolbar_box)
        # self.ids.toolbar_box += Animation(pos=(800, 800), duration=2, t='in_back')  # and then here
        level = 4.5
        if self.refresher:
            self.ids.spinner.active = True
            # time.sleep(0.2)
            # self.ids.spinner.active = False

        print(self.ids.scroll.scroll_y)
        if self.ids.scroll.scroll_y >= level:
            print("call refresher")
            self.refresher = True


