from email.mime import base
import requests
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.toast import toast
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior

from threading import Thread

import mysql.connector
import datetime

#FIXME: Need to work on Seat Selection Field (User Can Select Their Seat Number using Checkboxes)
baseUri = 'https://bus-reservation.vercel.app/api/v1/'

Builder.load_file("user/user.kv")

selected_trip_id = None
selected_seat = list()
passenger = 0
update_trip_summary = False
payment_method = None
Thread.daemon = True

class OptionCard(MDCard):
    icon = StringProperty(None)
    text = StringProperty(None)

class NoData(MDFloatLayout):
    text = "No Data"
    icon = "database"

class Seat(MDBoxLayout):
    text = StringProperty()

    def add_seat(self, checkbox, seat_no):
        global selected_seat, passenger, update_trip_summary
        if checkbox.state == "down":
            passenger += 1
            selected_seat.append(seat_no)
            update_trip_summary = True
        else:
            passenger -= 1
            selected_seat.remove(seat_no)
            update_trip_summary = True

class BusTicket(MDCard, RoundedRectangularElevationBehavior, ButtonBehavior):
    trip_id = StringProperty(None)
    departure_date = StringProperty(None)
    departure_time = StringProperty(None)
    seat = StringProperty(None)
    price = StringProperty(None)
    bus_name = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_press=lambda x: self.get_trip_id(self.trip_id))

    def get_trip_id(self, trip_id):
        global selected_trip_id
        selected_trip_id = trip_id

class PurchasedTicket(MDCard, RoundedRectangularElevationBehavior):
    booking_id = StringProperty(None)
    trip_id = StringProperty(None)
    destination = StringProperty(None)
    booking_date = StringProperty(None)
    price = StringProperty(None)
    bus_name = StringProperty(None)
    seat = StringProperty(None)
    paid_status = StringProperty(None)

class CustomTextField(MDTextField):
    pass

class TripSummary(MDBoxLayout):
    destination = StringProperty()
    departure_date = StringProperty()
    passenger = StringProperty("-")
    seat_no = StringProperty("-")
    unit_price = StringProperty()
    total_payment = StringProperty("0.00")

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
        self.trip_summary = None
        self.payment_summary = None
        self.threading = None

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
        self.ids.toolbar.title = "Booking"
        self.ids.toolbar.right_action_items = []

    def booking_location(self):
        self.set_list_locations()
        self.ids.scrn_booking_mngr.transition.direction = "up"
        self.ids.scrn_booking_mngr.current = "scrn_booking_location"
        self.ids.toolbar.title = "Choose Location"
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

    def booking_seat(self, trip_id):
        global selected_seat, passenger
        selected_seat = list()
        passenger = 0
        self.set_trip_summary(trip_id)
        self.ids.trip_summary_fld.clear_widgets()
        self.ids.trip_summary_fld.add_widget(
            MDExpansionPanel(
                content=self.trip_summary,
                panel_cls=MDExpansionPanelOneLine(
                    text="Trip Summary"
                )
            )
        )
        self.set_seat_layout(trip_id)
        self.ids.scrn_booking_mngr.transition.direction = "up"
        self.ids.scrn_booking_mngr.current = "scrn_seat_selection"
        self.ids.toolbar.title = "Select Seat"
        self.ids.toolbar.right_action_items = [
            ['arrow-left-bold', lambda x: self.booking_ticket()]
        ]

        self.threading = Thread(target=self.update_trip_summary)
        self.threading.start()

    def booking_payment(self):
        global passenger
        if passenger == 0:
            self.dialog = MDDialog(
                title="Missing Requirement",
                text="Please select a seat",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            self.set_payment_summary()
            self.ids.payment_detail.clear_widgets()
            self.ids.payment_detail.add_widget(
                MDExpansionPanel(
                    content=self.payment_summary,
                    panel_cls=MDExpansionPanelOneLine(
                        text="Trip Summary"
                    )
                )
            )
            self.ids.scrn_booking_mngr.transition.direction = "up"
            self.ids.scrn_booking_mngr.current = "scrn_payment"
            self.ids.toolbar.title = "Select Seat"
            self.ids.toolbar.right_action_items = [
                ['arrow-left-bold', lambda x: self.booking_ticket()]
            ]

    def check_out(self):
        global payment_method
        if not payment_method:
            self.dialog = MDDialog(
                title="Missing Requirement!",
                text="Please Select a payment method to continue",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            """ Add Record to tbl_booking and tbl_booking_detail """
            # Get user_id
            username = self.ids.nav_drawer_header.text
            sql = 'SELECT user_id FROM users WHERE user_name = %s'
            values = [username, ]
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()
            user_id = result[0]

            # Get total payment
            payment = float(self.payment_summary.total_payment)

            # Get booking date
            booking_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # For tbl_booking
            # print("For tbl_booking")
            # print(f"user_id: {user_id}")
            # print(f"payment: {payment}")
            # print(f"booking_date: {booking_date}")

            # Insert record into tbl_booking
            sql = 'INSERT INTO booking (user_id, payment, booking_date) ' \
                  'VALUES (%s, %s, %s)'
            values = [user_id, payment, booking_date, ]
            self.mycursor.execute(sql, values)
            self.mydb.commit()

            # Get booking_id from tbl_booking by fetching last row
            sql = 'SELECT id FROM booking ORDER BY id DESC LIMIT 1'
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            booking_id = result[0]

            # Get trip_id
            trip_id = selected_trip_id

            # Get price
            price = float(self.payment_summary.unit_price)

            # For tbl_booking_detail
            # print(f"For tbl_booking_detail")
            # print(f"trip_id: {trip_id}")
            # print(f"seat_id: {seat_id}")
            # print(f"price: {price}")

            # Insert records into tbl_booking_detail
            for x in range(passenger):
                # Get seat_id
                sql = 'SELECT id FROM bus_seat ' \
                      'WHERE seat_name = %s AND bus_id IN ' \
                      '(SELECT bus_id FROM trip ' \
                      'WHERE id = %s)'
                values = [selected_seat[x], trip_id, ]
                self.mycursor.execute(sql, values)
                result = self.mycursor.fetchone()
                seat_id = result[0]

                # Insert Record
                sql = 'INSERT INTO booking_detail (booking_id, trip_id, seat_id, price) ' \
                      'VALUES (%s, %s, %s, %s)'
                values = [booking_id, trip_id, seat_id, price, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

                # Update seat status
                sql = 'UPDATE bus_seat SET status = 0 ' \
                      'WHERE id = %s'
                values = [seat_id, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

                # Update trip available seat
                sql = 'UPDATE trip SET seat = seat - 1 ' \
                      'WHERE id = %s'
                values = [trip_id, ]
                self.mycursor.execute(sql, values)
                self.mycursor.commit()

            # Online Payment Method or Offline Payment Method
            if payment_method == "Online Payment":
                sql = 'INSERT INTO payment_online (booking_id, pay_date, cus_id) ' \
                      'VALUES (%s, %s, %s)'
                values = [booking_id, booking_date, user_id, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

                # Update Booking paid status
                sql = 'UPDATE booking SET status = 1 ' \
                      'WHERE id = %s'
                values = [booking_id, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

                self.dialog = MDDialog(
                    title="All Done",
                    text="Payment Successful!",
                    buttons=[
                        MDFlatButton(
                            text="Done",
                            on_release=lambda a: self.return_main_screen()
                        )
                    ]
                )
                self.dialog.open()
            else:
                sql = 'INSERT INTO payment_offline (booking_id, booking_date, cus_id) ' \
                      'VALUES (%s, %s, %s)'
                values = [booking_id, booking_date, user_id, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()

                self.dialog = MDDialog(
                    title="All Done",
                    text="Your ticket has been booked!",
                    buttons=[
                        MDFlatButton(
                            text="Done",
                            on_release=lambda a: self.return_main_screen()
                        )
                    ]
                )
                self.dialog.open()

    def search_tickets(self, location, depart_date):
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
            sql = 'SELECT loc_id FROM locations WHERE loc_name=%s'
            values = [location, ]
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()
            loc_id = result[0]

            #Get Departure Date
            temp = depart_date.split("-")
            temp.reverse()
            date = "-".join(temp)

            #Get Trip Detail
            sql = 'SELECT trip.id, trip.departure_date, trip.departure_time, trip.seat, bus.price, bus.bus_name ' \
                  'FROM trip ' \
                  'INNER JOIN bus ON trip.bus_id = bus.id ' \
                  'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                  'WHERE trip.loc_id=%s AND trip.departure_date=%s AND trip.status=1'
            values = [loc_id, date, ]
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchall()
            if not result:
                self.ids.search_count.text = "No Result"
                self.booking_ticket()
            else:
                count = self.mycursor.rowcount
                self.ids.search_ticket_detail.clear_widgets()
                self.ids.search_count.text = f"{count} trips found"
                for x in result:
                    ticket = BusTicket(
                        trip_id=f"{x[0]}",
                        departure_date=f"{x[1]}",
                        departure_time=f"{x[2]}",
                        seat=f"{x[3]}",
                        price=f"{x[4]}",
                        bus_name=f"{x[5]}",
                        on_release=lambda a: self.booking_seat(selected_trip_id)
                    )
                    self.ids.search_ticket_detail.add_widget(ticket)
                self.booking_ticket()

    def update_trip_summary(self):
        global update_trip_summary
        while True:
            if update_trip_summary:
                self.trip_summary.passenger = str(passenger)
                self.trip_summary.seat_no = ",".join(selected_seat)
                self.trip_summary.total_payment = str(passenger * float(self.trip_summary.unit_price))
                update_trip_summary = False
            if self.ids.scrn_booking_mngr.current != "scrn_seat_selection":
                return

    def set_trip_summary(self, trip_id):
        self.trip_summary = TripSummary()
        sql = 'SELECT locations.loc_name, trip.departure_date, trip.departure_time, bus.price ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id ' \
              'WHERE trip.id=%s'
        values = [trip_id, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchall()
        for x in result:
            self.trip_summary.destination = x[0]
            self.trip_summary.departure_date = f"{x[1]} {x[2]}"
            self.trip_summary.unit_price = f"{x[3]}"

    def set_payment_summary(self):
        # destination = StringProperty()
        # departure_date = StringProperty()
        # passenger = StringProperty("-")
        # seat_no = StringProperty("-")
        # unit_price = StringProperty()
        # total_payment = StringProperty("0.00")
        self.payment_summary = TripSummary()
        self.payment_summary.destination = self.trip_summary.destination
        self.payment_summary.departure_date = self.trip_summary.departure_date
        self.payment_summary.passenger = self.trip_summary.passenger
        self.payment_summary.seat_no = self.trip_summary.seat_no
        self.payment_summary.unit_price = self.trip_summary.unit_price
        self.payment_summary.total_payment = self.trip_summary.total_payment

    def set_seat_layout(self, trip_id):
        self.ids.seat_layout.clear_widgets()
        sql = 'SELECT seat_name, status ' \
              'FROM bus_seat ' \
              'WHERE bus_id IN (SELECT bus_id FROM trip WHERE id=%s)'
        values = [trip_id, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchall()
        for seat in result:
            if seat[1] == 1:
                self.ids.seat_layout.add_widget(
                    Seat(
                        text=f"{seat[0]}",
                        disabled=False,
                    )
                )
            else:
                self.ids.seat_layout.add_widget(
                    Seat(
                        text=f"{seat[0]}",
                        disabled=True,
                    )
                )

    def set_payment_method(self, checkbox, method):
        global payment_method
        if checkbox.state == "down":
            payment_method = method
        else:
            payment_method = None

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

    def ticket_home(self):
        sql = 'SELECT user_id FROM users ' \
              'WHERE user_name = %s'
        values = [self.ids.nav_drawer_header.text, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchone()
        user_id = result[0]
        self.set_purchased_ticket(user_id=user_id)

        self.ids.scrn_ticket_mngr.transition.direction = "right"
        self.ids.scrn_ticket_mngr.current = "scrn_ticket"
        self.ids.toolbar.right_action_items = []

    def set_purchased_ticket(self, user_id):
        self.ids.purchased_ticket.clear_widgets()
        # Check if user has booked any tickets
        booking = list()
        sql = 'SELECT id FROM booking WHERE user_id = %s'
        values = [user_id, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchall()
        if result:
            for x in result:
                booking.append(x[0])

        if not booking:
            self.ids.purchased_ticket.add_widget(NoData())
        else:
            # Get Purchased Ticket Detail
            for booking_id in booking:
                sql = 'SELECT payment, booking_date, status FROM booking ' \
                      'WHERE id = %s'
                values = [booking_id, ]
                self.mycursor.execute(sql, values)
                result = self.mycursor.fetchone()
                price = result[0]
                booking_date = result[1]
                status = result[2]

                paid_status = "Paid" if status == 1 else "Not Paid"

                seat = list()
                sql = 'SELECT seat_name FROM bus_seat ' \
                      'WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s)'
                values = [booking_id, ]
                self.mycursor.execute(sql, values)
                result = self.mycursor.fetchall()
                for x in result:
                    seat.append(x[0])

                sql = 'SELECT DISTINCT trip_id FROM booking_detail ' \
                      'WHERE booking_id = %s'
                values = [booking_id, ]
                self.mycursor.execute(sql, values)
                result = self.mycursor.fetchone()
                trip_id = result[0]

                sql = 'SELECT locations.loc_name, bus.bus_name FROM trip ' \
                      'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                      'INNER JOIN bus ON trip.bus_id = bus.id ' \
                      'WHERE trip.id IN (SELECT DISTINCT trip_id FROM booking_detail WHERE booking_id = %s)'
                values = [booking_id, ]
                self.mycursor.execute(sql, values)
                result = self.mycursor.fetchone()
                destination = result[0]
                bus_name = result[1]

                self.ids.purchased_ticket.add_widget(
                    PurchasedTicket(
                        booking_id=str(booking_id),
                        trip_id=str(trip_id),
                        destination=destination,
                        booking_date=str(booking_date),
                        price=str(price),
                        bus_name=bus_name,
                        seat=",".join(seat),
                        paid_status=paid_status,
                        on_release=lambda a=PurchasedTicket: self.show_purchased_summary(a)
                    )
                )
            self.ids.purchased_ticket.add_widget(
                MDLabel(
                    text=""
                )
            )

    def show_purchased_summary(self, ticket):
        purchased_summary = TripSummary()
        sql = 'SELECT locations.loc_name, trip.departure_date, trip.departure_time, bus.price ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id ' \
              'WHERE trip.id=%s'
        values = [ticket.trip_id, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchall()
        for x in result:
            purchased_summary.destination = x[0]
            purchased_summary.departure_date = f"{x[1]} {x[2]}"
            purchased_summary.unit_price = f"{x[3]}"

        purchased_summary.seat_no = ticket.seat
        purchased_summary.total_payment = ticket.price
        purchased_summary.passenger = str(len(ticket.seat.split(",")))

        self.ids.purchased_summary.clear_widgets()
        self.ids.purchased_summary.add_widget(purchased_summary)

        self.ids.scrn_ticket_mngr.transition.direction = "left"
        self.ids.scrn_ticket_mngr.current = "scrn_ticket_detail"
        self.ids.toolbar.title = "Ticket Detail"
        self.ids.toolbar.right_action_items = [
            ['arrow-left-bold', lambda a: self.ticket_home()]
        ]

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

    def return_main_screen(self):
        self.close_dialog()
        self.booking_home()

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

    # def show_trip_detail(self, trip_id, depart_date, depart_time, seat, price, bus):
    #     print(f"Trip ID: {trip_id}")
    #     print(f"Date: {depart_date}")
    #     print(f"Time: {depart_time}")
    #     print(f"Price: {price}")
    #     print(f"Bus: {bus}")
    #     print(f"Seat: {seat}")