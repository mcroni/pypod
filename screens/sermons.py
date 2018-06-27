from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from mat.list import OneLineAvatarListItem
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
import mat.snackbar as Snackbar
from kivy.uix.image import AsyncImage
from mat.list import ILeftBody
import _thread
from kivy.clock import Clock
import webbrowser
import requests
from bs4 import BeautifulSoup
Clock.max_iteration = 20
# i did this to prevent the app from crashing when looping through the images


""" chale release this lines when ready to deploy
this will activate the share intent in android"""
# from jnius import autoclass
# PythonActivity = autoclass('org.renpy.android.PythonActivity')
# Intent = autoclass('android.content.Intent')
# String = autoclass('java.lang.String')


class AudioButton(OneLineAvatarListItem):
    def __init__(self,**kwargs):
        super(AudioButton,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print(str(self.text))
            a = DownPop(title=str(self.text))
            self.link = 'http://point3hub.com/mcroni/sermons/{}'.format(str(self.text))
            print(self.link)
            a.open()

        super(AudioButton, self).on_touch_down(touch)


class DownPop(Popup):
    def __init__(self,**kwargs):
        super(DownPop,self).__init__(**kwargs)
        self.source = 'http://point3hub.com/mcroni/sermons/{}'.format(str(self.title))

    def load_play(self):
        _thread.start_new_thread(self.play, ('name',))

    def play(self,name):
        """maybe using clock instead of the thread may be a good idea
        implement that in v0.9"""
        if self.ids.play_stop.text == 'Play':
            self.sound = SoundLoader.load(self.source)
            self.sound.play()
            self.ids.play_stop.text = "Stop"
        else:
            self.ids.play_stop.text = "Play"
            self.sound.unload()
            self.sound.stop()

    def download(self):
        try:
            webbrowser.open(self.source)
        except ConnectionError:
            pass



    # def share(self):
    #     intent = Intent()
    #     intent.setAction(Intent.ACTION_SEND)
    #     intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(self.source)))
    #     intent.setType('text/plain')
    #     chooser = Intent.createChooser(intent, String('Share...'))
    #     PythonActivity.mActivity.startActivity(chooser)



class Sermons(Screen):
    scroller = ObjectProperty(None)
    grid = ObjectProperty(None)
    passed = []
    links = []

    def __init__(self, **kwargs):
        super(Sermons, self).__init__(**kwargs)


    def load(self):
        _thread.start_new_thread(self.list_files, ('name',))
        self.ids.search_input.bind(text=self.some_func)

    def list_files(self, name):
        print('display thread')
        self.ids.grid.clear_widgets()
        self.ids.spinner.active = True
        url = 'http://point3hub.com/mcroni/sermons/'
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
                if link.get('href').endswith('.mp3'):
                    self.passed.append(link.get('href'))
            self.ids.spinner.active = False

            print(self.passed)
            for track in self.passed:
                src = 'http://point3hub.com/mcroni/sermons/{}'.format(track)
                print(src)
                self.links.append(src)
                self.album = AudioButton(text=str(track))
                self.album.add_widget(Photo(source='tower.png'))
                self.ids.grid.clear_widgets()
                self.ids.grid.add_widget(self.album)
            self.ids.spinner.active = False
            print(self.links)

    def some_func(self, *args):
        returned_name = self.ids.search_input.text
        self.ids.grid.clear_widgets()
        for track in self.passed:
            if track.startswith(returned_name):
                self.album = AudioButton(text=str(track))
                self.album.add_widget(Photo(source='tower.png'))

                self.ids.grid.add_widget(self.album)
        print(len(self.ids.grid.children))
        if len(self.ids.grid.children) == 0:
            self.show_example_snackbar('simple')

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar.make("Sorry Sermon Not Found :-(", duration=1)


class Photo(ILeftBody, AsyncImage):
    pass