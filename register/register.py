import requests
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import datetime

baseUri = 'https://bus-reservation.vercel.app/api/v1/'

import mysql.connector

Builder.load_file("register/register.kv")

class RegisterTextField(MDTextField):
    pass

class RegisterWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="P@ssw0rd",
            database="bus_python",
            port=3307
        )
        self.mycursor = self.mydb.cursor()

        self.dialog = None

    def register(self, username, password, email):
        """ Insert User Information into Database """
        res = requests.get('%sget-users'%(baseUri)).json()
        # sql = 'SELECT user_name, email FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        if res['is_success']:
            result = res['data']
            user_list = []
            email_list = []
            for x in result:
                user_list.append(x['user_name'])
                email_list.append(x['email'])
            if username in user_list:
                self.ids.username_fld.error = True
            elif password == "":
                self.ids.password_fld.error = True
            elif email in email_list:
                self.ids.email_fld.error = True
            else:
                self.ids.username_fld.error = False
                self.ids.password_fld.error = False
                self.ids.email_fld.error = False
                try:
                    # create_date = datetime.now().strftime("%Y-%m-%d")
                    # sql = 'INSERT INTO users (user_name, user_pass, email, created_date)' \
                    #     'VALUEs (%s, %s, %s, %s)'
                    # values = [username, password, email, create_date, ]
                    # self.mycursor.execute(sql, values)
                    # self.mydb.commit()
                    req = {
                        'user_name': username,
                        'user_pass': password,
                        'email': email
                    }
                    res = requests.post('%sregister'%(baseUri), json=req).json()
                    if res['is_success']:
                        self.ids.username_fld.text = ""
                        self.ids.password_fld.text = ""
                        self.ids.email_fld.text = ""
                        self.dialog = MDDialog(
                            title="Success!",
                            text="Account created successfully!",
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    md_bg_color=(0, 0, 0, 0),
                                    on_release=self.close_dialog
                                )
                            ]
                        )
                        self.dialog.open()
                    else:
                        raise Exception
                except:
                    self.dialog = MDDialog(
                        title="Error!",
                        text="Please try again later!",
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                md_bg_color=(0, 0, 0, 0),
                                on_release=self.close_dialog()
                            )
                        ]
                    )
                    self.dialog.open()
                    

    def goto_sign_in(self):
        """ Return to Sign In Page """
        self.parent.parent.transition.direction = "right"
        self.parent.parent.current = "scrn_login"
        self.ids.username_fld.text = ""
        self.ids.password_fld.text = ""
        self.ids.email_fld.text = ""
        self.ids.username_fld.error = False
        self.ids.password_fld.error = False
        self.ids.email_fld.error = False

    def close_dialog(self, *args):
        """ Close Active Dialog """
        self.dialog.dismiss(force=True)

