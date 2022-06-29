from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager
# import mysql.connector
import requests

baseUri = 'https://bus-reservation.vercel.app/api/v1/'

Builder.load_file("login/login.kv")

class LoginWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     passwd="P@ssw0rd",
        #     database="bus_python",
        #     port=3307
        # )
        # self.mycursor = self.mydb.cursor()

    def validate_user(self, username, password):
        res = requests.get('%sget-user/%s' %(baseUri, username)).json()
        if res['is_success']:
            target_user = res['data']
            if not target_user:
                self.ids.username_fld.error = True
            else:
                self.ids.username_fld.error = False
                if target_user['user_pass'] != password:
                    self.ids.password_fld.error = True
                else:
                    self.ids.password_fld.error = False
                    if target_user['user_name']== "User":
                        self.parent.parent.transition.direction = "left"
                        self.parent.parent.current = "scrn_user"
                        self.parent.parent.parent.ids.scrn_user.children[0] \
                            .ids.nav_drawer_header.text = username
                        self.ids.username_fld.text = ""
                        self.ids.password_fld.text = ""
                        toast(f"Logged in as {username}!")
                    else:
                        self.parent.parent.transition.direction = "left"
                        self.parent.parent.current = "scrn_admin"
                        self.parent.parent.parent.ids.scrn_admin.children[0] \
                            .ids.nav_drawer_header.text = username
                        self.ids.password_fld.text = ""
                        self.ids.username_fld.text = ""
                        toast(f"Logged in as {username}!")
    def goto_register(self):
        self.parent.parent.transition.direction = "left"
        self.parent.parent.current = "scrn_register"
        self.ids.username_fld.text = ""
        self.ids.password_fld.text = ""