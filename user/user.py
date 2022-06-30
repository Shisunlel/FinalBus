from email.mime import base
import requests
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast

import mysql.connector

baseUri = 'https://bus-reservation.vercel.app/api/v1/'

Builder.load_file("user/user.kv")

class OptionCard(MDCard):
    icon = StringProperty(None)
    text = StringProperty(None)

class CustomTextField(MDTextField):
    pass

class UserWindow(MDBoxLayout):
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

        self.location_items = []
        self.dialog = None
        self.departure_date = None
        self.return_date = None
        self.dob_date = None
        self.return_date = None
        self.get_locations()

    def get_locations(self):
        # sql = 'SELECT loc_name FROM locations'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        res = requests.get('%sget-locations'%(baseUri)).json()
        result = res['data']
        for x in result:
            self.location_items.append(x)

    def booking_home(self):
        self.ids.scrn_booking_mngr.transition.direction = "down"
        self.ids.scrn_booking_mngr.current = "scrn_booking_home"
        self.ids.toolbar.right_action_items = []

    def booking_location(self):
        self.set_list_locations()
        self.ids.scrn_booking_mngr.transition.direction = "up"
        self.ids.scrn_booking_mngr.current = "scrn_booking_location"
        self.ids.toolbar.right_action_items = [
            ['arrow-left-bold', lambda x: self.booking_home()]
        ]

    def booking_ticket(self):
        self.ids.scrn_booking_mngr.transition.direction = "up"
        self.ids.scrn_booking_mngr.current = "scrn_search_ticket"
        self.ids.toolbar.title = "Search"
        self.ids.toolbar.right_action_items = [
            ['arrow-left-bold', lambda x: self.booking_home()]
        ]

    #FIXME: Let User Choose How many Seat They want after clicking on a trip
    def search_tickets(self, location, depart_date):
        #Check for requirements
        if location == "" or depart_date == "":
            self.dialog = MDDialog(
                title="Missing Requirement!",
                text="Please Input Location and Departure Date to continue!",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            #Get Location ID
            # sql = 'SELECT loc_id FROM locations WHERE loc_name=%s'
            # values = [location, ]
            # self.mycursor.execute(sql, values)
            res = requests.get('%sget-location-by-name/%s' %(baseUri, location)).json()
            result = res['data']
            loc_id = result['loc_id']

            #Get Departure Date
            temp = depart_date.split("-")
            temp.reverse()
            date = "-".join(temp)

            #Get Trip Detail
            # sql = 'SELECT trip.id, trip.departure_date, trip.departure_time, trip.seat, bus.price, bus.bus_name ' \
            #       'FROM trip ' \
            #       'INNER JOIN bus ON trip.bus_id = bus.id ' \
            #       'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
            #       'WHERE trip.loc_id=%s AND trip.departure_date=%s'
            # values = [loc_id, date, ]
            # self.mycursor.execute(sql, values)
            res = requests.get('%sget-trips-by-loc-and-departure/%s/%s' %(baseUri, loc_id, date)).json()
            result = res['data']
            if not result:
                self.ids.search_count.text = "No Result"
                self.booking_ticket()
            else:
                count = self.mycursor.rowcount
                self.ids.search_ticket_detail.clear_widgets()
                self.ids.search_count.text = f"{count} trips found"
                for x in result:
                    self.ids.search_ticket_detail.add_widget(
                        BusTicket(
                            departure_date=f"{x['departure_date']}",
                            departure_time=f"{x['departure_time']}",
                            seat=f"{x['seat']}",
                            price=f"{x['price_per_seat']}",
                            bus_name=f"{x['bus_name']}"
                        )
                    )
                self.booking_ticket()

    def set_list_locations(self):
        """ Show Location Menu """
        self.ids.rv.clear_widgets()

        def add_location_items(location):
            self.ids.rv.add_widget(
                OneLineListItem(
                    text=location,
                    font_style="H6",
                    divider="Inset",
                    on_release=lambda x: location_callback(location)
                )
            )

        for x in self.location_items:
            add_location_items(x[0])

        def location_callback(location):
            self.ids.location_fld.text = location
            self.booking_home()

    def departure_date_picker(self):
        self.departure_date = MDDatePicker(
            primary_color=(0,0,0,1),
            selector_color=(0,0,0,1),
            text_button_color=(0,0,0,1),
            text_current_color=(0,0,0,1)
        )
        self.departure_date.bind(on_save=self.save_departure_date, on_cancel=self.close_departure_date_picker)
        self.departure_date.open()

    def save_departure_date(self, instance, value, date_range):
        date = value.strftime("%d-%m-%Y")
        self.ids.departure_fld.secondary_text = str(date)

    def close_departure_date_picker(self, instance, value):
        self.departure_date.dismiss(force=True)

    def return_date_picker(self):
        self.return_date = MDDatePicker(
            primary_colorw=(0,0,0,1),
            selector_color=(0,0,0,1),
            text_button_color=(0,0,0,1),
            text_current_color=(0,0,0,1)
        )
        self.return_date.bind(on_save=self.save_return_date, on_cancel=self.close_return_date_picker)
        self.return_date.open()

    def save_return_date(self, instance, value, date_range):
        date = value.strftime("%d-%m-%Y")
        self.ids.return_fld.secondary_text = str(date)

    def close_return_date_picker(self, instance, value):
        self.return_date.dismiss(force=True)

    def dob_date_picker(self):
        self.dob_date = MDDatePicker(
            min_year=1950,
            max_year=2050,
            primary_color=(0, 0, 0, 1),
            selector_color=(0, 0, 0, 1),
            text_button_color=(0, 0, 0, 1),
            text_current_color=(0, 0, 0, 1),
            input_field_text_color=(0,0,0,1)
        )
        self.dob_date.bind(on_save=self.save_dob_date, on_cancel=self.close_dob_date_picker)
        self.dob_date.open()

    def save_dob_date(self, instance, value, date_range):
        date = value.strftime("%d-%m-%Y")
        self.ids.dob_fld.text = str(date)

    def close_dob_date_picker(self, instance, value):
        self.dob_date.dismiss(force=True)

    def goto_main_screen(self):
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "main_scrn"

    def account_edit_profile(self):
        user_name = self.ids.nav_drawer_header.text
        # sql = 'SELECT first_name, last_name, phone, email, date_of_birth FROM users ' \
        #       'WHERE user_name = %s'
        # values = [user_name, ]
        # self.mycursor.execute(sql, values)
        res = requests.get('%sget-user/%s'%(baseUri, user_name)).json()
        # result = self.mycursor.fetchall()
        for x in res['data']:
            if x['first_name'] and x['last_name']:
                self.ids.first_name_fld.text = x['first_name']
                self.ids.last_name_fld.text = x['last_name']
            else:
                self.ids.first_name_fld.text = ""
                self.ids.last_name_fld.text = ""
            if x['phone']:
                self.ids.phone_fld.text = x['phone']
            else:
                self.ids.phone_fld.text = ""
            if x['email']:
                self.ids.email_fld.text = x['email']
            else:
                self.ids.email_fld.text = ""
            if x['date_of_birth']:
                self.ids.dob_fld.text = str(x['date_of_birth'])
            else:
                self.ids.dob_fld.text = ""
        self.ids.scrn_account_mngr.current = "scrn_edit_profile"
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_setting"

    def account_settings(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_setting"
        self.ids.scrn_account_mngr.current = "scrn_account_settings"

    def update_password(self, old_pass, new_pass, confirm_pass):
        if old_pass == "" or new_pass == "" or confirm_pass == "":
            toast("All Field Required")
        else:
            username = self.ids.nav_drawer_header.text
            # sql = 'SELECT user_pass FROM users WHERE user_name=%s'
            # values = [username, ]
            # self.mycursor.execute(sql,values)
            # result = self.mycursor.fetchall()
            # password = result[0][0]
            res = requests.get('%sget-user/%s' %(baseUri, username)).json()
            password = res['user_pass']
            if old_pass == password:
                if new_pass == confirm_pass:
                    try:
                        # sql = 'UPDATE users SET ' \
                        #       'user_pass = %s ' \
                        #       'WHERE user_name = %s'
                        # values = [new_pass, username, ]
                        # self.mycursor.execute(sql, values)
                        # self.mydb.commit()
                        data = {
                            "user_pass": new_pass,
                            "user_name": username
                        }
                        res = requests.post('%supdate-password' %(baseUri), json= data).json()
                        if not res['is_success']:
                            raise Exception
                    except:
                        self.dialog = MDDialog(
                            title="Error!",
                            text="Cannot update your password!",
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    on_release=self.close_dialog
                                )
                            ]
                        )
                        self.dialog.open()
                        self.ids.old_pass.text = ""
                        self.ids.new_pass.text = ""
                        self.ids.confirm_pass.text = ""
                    else:
                        self.dialog = MDDialog(
                            title="Success!",
                            text="Password Update Successfully!",
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    on_release=self.close_dialog
                                )
                            ]
                        )
                        self.dialog.open()
                        self.ids.old_pass.text = ""
                        self.ids.new_pass.text = ""
                        self.ids.confirm_pass.text = ""
                else:
                    self.ids.confirm_pass.error = True
            else:
                self.ids.old_pass.error = True

    def update_info(self, first_name, last_name, phone, email, dob):
        if first_name == "":
            f_name = None
        else:
            f_name = first_name
        if last_name == "":
            l_name = None
        else:
            l_name = last_name
        if phone == "":
            phone_num = None
        else:
            phone_num = phone
        if dob == "":
            u_dob = None
        else:
            value = dob.split("-")
            date = []
            for x in range(len(value)-1, -1, -1):
                date.append(value[x])
            u_dob = "-".join(date)
        if f_name is None and l_name is not None or f_name is not None and l_name is None:
            toast("Both First name and Last name required!")
        else:
            if email == "":
                self.ids.email_fld.error = True
            else:
                email_addr = email
                try:
                    username = self.ids.nav_drawer_header.text
                    # sql = 'UPDATE users SET ' \
                    #       'first_name=%s, last_name=%s, phone=%s, email=%s, date_of_birth=%s ' \
                    #       'WHERE user_name=%s'
                    # values = [f_name, l_name, phone_num, email_addr, u_dob, username, ]
                    # self.mycursor.execute(sql, values)
                    # self.mydb.commit()
                    data = {
                    "user_name": username,
                    "first_name": f_name,
                    "last_name": l_name,
                    "phone": phone_num,
                    "email": email_addr,
                    "date_of_birth": u_dob
                    }
                    res = requests.post('%supdate-info' %(baseUri), json=data).json()
                    if not res['is_success']:
                        raise Exception
                except:
                    self.dialog = MDDialog(
                        title="Error!",
                        text="Cannot update your information!",
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()
                else:
                    self.dialog = MDDialog(
                        title="Success!",
                        text="Your information has been updated!",
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()
                    self.goto_main_screen()

    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)

    def show_logout_dialog(self):
        self.dialog = MDDialog(
            title="Are you sure you want to logout?",
            buttons=[
                MDFlatButton(
                    text="Yes",
                    on_release=lambda x: self.logout()
                ),
                MDFlatButton(
                    text="No",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def logout(self):
        self.parent.parent.transition.direction = "right"
        self.parent.parent.current = "scrn_login"
        self.close_dialog()