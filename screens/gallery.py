from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from mat.list import MDList
from mat.grid import SmartTile,SmartTileWithLabel2
from mat.button import MDFloatingActionButton
from kivy.app import App
from kivy.uix.image import AsyncImage
import _thread
from kivy.clock import Clock
import requests
from PIL import Image as PI
from bs4 import BeautifulSoup
from io import BytesIO
import webbrowser
from kivy.uix.image import AsyncImage

# i did this to prevent the app from crashing when looping through the images
Clock.max_iteration = 15


class Gallery(Screen):
    grid = ObjectProperty(None)
    passed = []

    def __init__(self,**kwargs):
        super(Gallery,self).__init__(**kwargs)

    def load(self):
        _thread.start_new_thread(self.list_files,('name',))

    def list_files(self,name):
        print('display thread')
        self.ids.grid.clear_widgets()
        self.ids.spinner.active = True
        url = 'http://point3hub.com/mcroni/albums/'
        try:
            r = requests.get(url)
        except requests.packages.urllib3.exceptions.ProtocolError:
            print('cant connect')
            self.ids.spinner.active = False
            img = AsyncImage(source='network.png',keep_ratio= False,allow_stretch=True)
            self.ids.grid.add_widget(img)

        else:
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            for link in soup.find_all('a'):
                if link.get('href').endswith('.jpg'):
                    self.passed.append(link.get('href'))
            self.ids.spinner.active = False

            # print(self.passed)
            for pic in self.passed:
                src = 'http://point3hub.com/mcroni/albums/{}'.format(pic)
                print(src)
                # self.p.append(src)
                self.album = SM(source=str(src))
                self.ids.grid.clear_widgets()
                self.ids.grid.add_widget(self.album)
            self.ids.spinner.active = False
            # print(self.links)


class SM(SmartTileWithLabel2):

    def __init__(self,**kwargs):
        super(SM,self).__init__(**kwargs)

    def load(self):
        _thread.start_new_thread(self.save, ('name',))

    def save(self,name):
        print(self.source)
        """lets reserve u for v1.1, add folder functionality so that
        the images gets stored in a special gbee folder"""
        filename = self.source[35:]
        r = requests.get(self.source)
        i = PI.open(BytesIO(r.content))
        i.save(filename)
        print('downloaded', filename)