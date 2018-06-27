from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image,AsyncImage
from kivymd.button import MDIconButton
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch
from kivymd.navigationdrawer import NavigationDrawer
from kivymd.theming import ThemeManager
from kivy.core.window import Window as Win
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from garden import *
from screens.settings import *
from kivymd.selectioncontrols import MDCheckbox
from kivymd.list import OneLineAvatarIconListItem
from kivymd.snackbar import Snackbar
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
import pyjokes
import webbrowser
from kivy.storage.jsonstore import JsonStore
favourites_store = JsonStore('fav.json')

class TollTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(TollTab, self).__init__(**kwargs)


class CashierTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(CashierTab, self).__init__(**kwargs)

    def show_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Enter your password and choose ACTIVe for Service Provider\'s Admin. "
                               "This feature locks command controls to restrict cashiers from withdrawing money from your account. "
                          "Choose INACTIVE to deactivate this feature",
                          )
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Cashier Restriction Config.",
                               content=content,
                               size_hint=(.9, None),
                               height=dp(300),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': 'Active'},
        {'viewclass': 'MDMenuItem',
         'text': 'Inactive'},
    ]

class ManagementTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(ManagementTab, self).__init__(**kwargs)


class InvestmentsTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(InvestmentsTab, self).__init__(**kwargs)

    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': '30 Days'},
        {'viewclass': 'MDMenuItem',
         'text': '60 Days'},
        {'viewclass': 'MDMenuItem',
         'text': '90 Days'},
        {'viewclass': 'MDMenuItem',
         'text': '120'},
        {'viewclass': 'MDMenuItem',
         'text': '150 Days'},
        {'viewclass': 'MDMenuItem',
         'text': '2 Years'},
    ]


class RechargeTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(RechargeTab, self).__init__(**kwargs)


class ImportTab(BoxLayout, AndroidTabsBase):
    def __init__(self, **kwargs):
        super(ImportTab, self).__init__(**kwargs)

    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': 'National'},
        {'viewclass': 'MDMenuItem',
         'text': 'Voters'},
        {'viewclass': 'MDMenuItem',
         'text': 'NHIS'},
        {'viewclass': 'MDMenuItem',
         'text': 'Drivers'},
        {'viewclass': 'MDMenuItem',
         'text': 'Passport'},
    ]


class ATab(AndroidTabs):
    pass

class ContactPhoto(ILeftBody,AsyncImage):
    pass

class AvatarSampleWidget(ILeftBody, AsyncImage):
    def __init__(self,**kwargs):
        # self.source = './assets/avatar.png'
        super(AvatarSampleWidget,self).__init__(**kwargs)

class ImageButton(ButtonBehavior,Image):
    pass


class PodList(OneLineAvatarIconListItem):
    def __init__(self,**kwargs):
        self.data = ""
        super(PodList,self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print('touched')
            # print(self.data)
            App.get_running_app().podcast_data = self.data
            App.get_running_app().root.next_screen("play_screen")
        return super(PodList, self).on_touch_down(touch)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.state = "pause"
    def get_joke(self):
        joke = pyjokes.get_joke(category="all")
        self.ids.get_a_joke_text.text = joke

    def pause_play(self):
        print("root play called")
        if self.state == "pause":
            self.ids.play_button.source = "./assets/pause (3).png"
            self.ids.play_button.size_hint =(0.7,None)
            self.ids.play_button.height = dp(500)

            self.state = "play"
        else:
            self.ids.play_button.source = "./assets/play (2).png"
            self.ids.play_button.size_hint =(0.7,None)
            self.ids.play_button.height = dp(500)
            self.state = "pause"

    def refresh(self):
        print(instance)

    def share(self):
        print(self.ids.get_a_joke_text.text)
        from jnius import autoclass
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        subject = 'PyPod Daily Jokes from Pyjokes'
        intent.putExtra(Intent.EXTRA_SUBJECT, subject)
        joke = self.ids.get_a_joke_text.text
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(joke)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String('Share...'))
        PythonActivity.mActivity.startActivity(chooser)
        

    def like(self):
        print("liking joke")
        Snackbar(text="You liked this joke!").show()


    def pyjokes(self):
        print(self.ids.get_a_joke_text.text)
        webbrowser.open("https://github.com/pyjokes/pyjokes")


class PlayScreen(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.state = "pause"
        self.source = ""
    def pause_play(self):
        print("root play called")
        if self.state == "pause":
            self.ids.play_button_.source = "./assets/pause (3).png"
            self.state = "play"
            from jnius import autoclass
            from time import sleep
            MediaPlayer = autoclass('android.media.MediaPlayer')
            mPlayer = MediaPlayer()
            mPlayer.setDataSource('{}'.format(self.source))
            mPlayer.prepare()
            duration = mPlayer.getDuration()
            if self.ids.play_stop.text == 'Play':
                # mPlayer.prepare()
                self.ids.play_stop.text = 'Stop'
                mPlayer.start()
                # print 'current position:', mPlayer.getCurrentPosition()
                sleep(int(duration))
            elif self.ids.play_stop.text == 'Stop':
                self.ids.play_stop.text = 'Play'
                # sleep(3)
                mPlayer.pause()
        else:
            self.ids.play_button_.source = "./assets/play (2).png"
            self.state = "pause"

    def load_info(self):
        data = App.get_running_app().podcast_data
        title = data['title']
        duration = data['itunes_duration']
        authors = data['authors']
        summary = data['summary']
        summary_detail = data['summary_detail']
        stream_url = data['links'][1]['href']
        self.source = stream_url
        # print(data['links'][1]['href'])
        # print(data['link'])
        # print(data.keys())



class GbeeRoot(BoxLayout):
    def __init__(self,**kwargs):
        super(GbeeRoot,self).__init__(**kwargs)
        self.screen_list = []
        self.provider = ""

    def next_screen(self, neoscreen):
        self.screen_list.append(self.ids.gbee_screen_manager.current)
        print(self.provider)
        print(self.screen_list)

        if self.ids.gbee_screen_manager.current == neoscreen:
            cur_screen = self.ids.gbee_screen_manager.get_screen(neoscreen)
        else:
            self.ids.gbee_screen_manager.current = neoscreen

    def go_to(self, neoscreen):
        self.ids.gbee_screen_manager.current = neoscreen

    def onBackBtn(self):
        # check if there are screens we can go back to
        if self.screen_list:
            currentscreen = self.screen_list.pop()
            self.ids.gbee_screen_manager.current = currentscreen
            # Prevents closing of app
            return True
        # no more screens to go back to, close app
        return False

class Drawer(NavigationDrawer):
    def __init__(self,**kwargs):
        super(Drawer, self).__init__(**kwargs)


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDIconButton):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            print(str(self.provider))
            print(self.liked)
            Snackbar(text="You liked this podcast!").show()
            return True
        super(IconRightSampleWidget, self).on_touch_down(touch)



class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class Jarvis(App):
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        Win.bind(on_keyboard=self.onBackBtn)
        self.my_screenmanager = ScreenManager()
        self.podcast_date = ""
        main_screen = MainScreen(name='screen1')
        settings_screen = PythonBytesScreen(name='settings_screen')
        play_screen = PlayScreen(name="play_screen")
        screen_lists = [main_screen,settings_screen,play_screen]
        for screen in screen_lists:
            self.my_screenmanager.add_widget(screen)

    def build(self):
        self.title = "pyPod"
        self.deger = 0
        from kivy.core.window import Window
        Window.size = (400, 600)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Indigo'
        self.nav_drawer = Drawer()
        return GbeeRoot()

    def onBackBtn(self, window, key, *args):
        if key == 27:
            return self.root.onBackBtn()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def spin(self, nesne):
        if self.deger == 0:
            self.say += 1
            res = './assets/a' + str(self.say) + '.png'
            # self.root.ids.btn1.background_normal = res
            # print(self.root.ids.btn1.background_normal)
            if self.say == 5:
                Clock.unschedule(self.spin)
                self.img = Button(size_hint=(1, 1), background_color=[0.1,
                                                                      0.1,
                                                                      0.1,
                                                                      0.3])
                # self.root.add_widget(self.img, index=10)
                # self.root.ids.bottomsheet.add_widget(self.img,index=10)
                self.animate1()
        elif self.deger == 1:
            Clock.unschedule(self.triger)
            self.say -= 1
            res = './assets/a' + str(self.say) + '.png'
            # self.root.ids['btn1'].background_normal = res
            if self.say == 1:
                Clock.unschedule(self.spin)
                # self.root.ids.bottomsheet.remove_widget(self.img)
                self.animate1()

    def triger(self, *args):
        if self.deger == 0:
            self.say = 0
            Clock.schedule_interval(self.spin, 0.03)
        elif self.deger == 1:
            self.say = 6
            Clock.schedule_interval(self.spin, 0.03)

    def triger1(self, *args):

        if self.deger == 1:
            self.triger()

    def kaydir(self, *args):
        if round(self.app.ids.slid1.value * 100) > 16.0:
            self.animslide1()

    def animslide1(self, *args):
        self.key2 = 3
        self.menu = 1
        Clock.unschedule(self.menuslide2)
        animation4 = Animation(pos_hint={'center_x': 0.5,
                                         'center_y': 0.5}, t='out_quad', duration=0.2)
        animation4.start(self.root.ids['slide'])
        animation6 = Animation(pos_hint={'top': 1}, t='out_quad', duration=0.1)
        animation6.start(self.root.ids['bar'])
        animation7 = Animation(pos_hint={'center_x': 0.5,
                                         'center_y': 0.34}, t='out_quad', duration=0.1)
        animation7.start(self.app.ids.scr1)
        self.app.ids.konu.text = 'AYARLAR'
        self.app.ids.konu_icon.background_normal = 'set.png'
        self.rak = 1
        self.app.ids.slid1.pos_hint = {'center_x': -1,
                                       'center_y': -1}
        Clock.schedule_interval(self.menuslide1, 0.04)

    def menuslide1(self, *args):
        self.rak += 1
        self.root.ids.menu_icon.background_normal = 'menu' + str(self.rak) + '.png'
        if self.rak == 5:
            Clock.unschedule(self.menuslide1)
            self.val = self.root.ids.slid.value

    def animate1(self):
        if self.deger == 0:
            print(self.root.ids.main_screen.ids.btn2)
            animation1 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.2}, t='out_bounce', duration=0.4)
            animation1 &= Animation(size=(230, 230))
            animation1 += Animation(size=(230, 230))
            animation1.start(self.root.ids.main_screen.ids.btn2)
            animation2 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.3}, t='out_bounce', duration=0.6)
            animation2 &= Animation(size=(230, 230))
            animation2 += Animation(size=(230, 230))
            animation2.start(self.root.ids.main_screen.ids.btn3)
            animation6 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.4}, t='out_bounce', duration=0.8)
            animation6 &= Animation(size=(230, 230))
            animation6 += Animation(size=(230, 230))
            animation6.start(self.root.ids.main_screen.ids.btn4)
            animation3 = Animation(pos_hint={'center_x': 0.6,
                                             'center_y': 0.2}, t='out_bounce', duration=0.4)
            animation3 &= Animation(size=(230, 230))
            animation3 += Animation(size=(230, 230))
            # animation3.start(self.root.ids.main_screen.ids.lab1)
            animation4 = Animation(pos_hint={'center_x': 0.6,
                                             'center_y': 0.3}, t='out_bounce', duration=0.6)
            animation4 &= Animation(size=(230, 230))
            animation4 += Animation(size=(230, 230))
            # animation4.start(self.root.ids.main_screen.ids.lab2)
            animation5 = Animation(pos_hint={'center_x': 0.65,
                                             'center_y': 0.4}, t='out_bounce', duration=0.8)
            animation5 &= Animation(size=(230, 230))
            animation5 += Animation(size=(230, 230))
            # animation5.start(self.root.ids.main_screen.ids.lab3)
            self.root.ids.main_screen.ids.slid1.pos_hint = {'center_x': -1,
                                            'center_y': -1}
            self.deger = 1
        elif self.deger == 1:
            animation1 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.066}, t='out_bounce', duration=0.5)
            animation1 &= Animation(size=(230, 230))
            animation1 += Animation(size=(230, 230))
            animation1.start(self.root.ids.main_screen.ids.btn2)
            animation2 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.066}, t='out_bounce', duration=0.5)
            animation2 &= Animation(size=(230, 230))
            animation2 += Animation(size=(230, 230))
            animation2.start(self.root.ids.main_screen.ids.btn3)
            animation6 = Animation(pos_hint={'center_x': 0.8,
                                             'center_y': 0.066}, t='out_bounce', duration=0.5)
            animation6 &= Animation(size=(230, 230))
            animation6 += Animation(size=(230, 230))
            animation6.start(self.root.ids.main_screen.ids.btn4)
            animation3 = Animation(pos_hint={'center_x': -1,
                                             'center_y': 0.2}, t='out_bounce', duration=0.5)
            animation3 &= Animation(size=(230, 230))
            animation3 += Animation(size=(230, 230))
            # animation3.start(self.root.ids.main_screen.ids.lab1)
            animation4 = Animation(pos_hint={'center_x': -1,
                                             'center_y': 0.3}, t='out_bounce', duration=0.7)
            animation4 &= Animation(size=(230, 230))
            animation4 += Animation(size=(230, 230))
            # animation4.start(self.root.ids.main_screen.ids.lab2)
            animation5 = Animation(pos_hint={'center_x': -1,
                                             'center_y': 0.4}, t='out_bounce', duration=0.9)
            animation5 &= Animation(size=(230, 230))
            animation5 += Animation(size=(230, 230))
            # animation5.start(self.root.ids.main_screen.ids.lab3)
            self.root.ids.main_screen.ids.slid1.pos_hint = {'center_x': 0.1,
                                            'center_y': -1}
            self.deger = 0

    # def get_joke(self):
    #     joke = pyjokes.get_joke()
    #     print(self.root.ids.get_a_joke_text)
    #     print(self.my_screenmanager.screens)
        # print(joke)
if __name__=="__main__":
    Jarvis().run()
