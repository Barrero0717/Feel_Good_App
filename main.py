import imp
from time import strftime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
import requests
from datetime import datetime

Builder.load_file("desing.kv")

url = "https://www.affirmations.dev/"

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        
    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.transition.direction = "left"
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong user or password!"
    
    def forgot_password(self):
        self.manager.current = "under_construction"        
                         
class RootWidget(ScreenManager):
    pass

class SignUpScreen (Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")} 
        
        with open("users.json", "w") as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"
        
class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
    def get_quote(self):
        request = requests.get(url)
        response = json.loads(request.content)
        self.ids.quote.text = response["affirmation"]

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class UnderConstruction(Screen):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()