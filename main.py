import datetime
from time import strftime

from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
import sqlite3 as sql
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
Window.size = (360, 770)  #(1080, 2340)


class AddIngredient(FakeRectangularElevationBehavior, FloatLayout):
    names = ObjectProperty()
    price = ObjectProperty()
    quantity = ObjectProperty()
    pcs = ObjectProperty()
    ml = ObjectProperty()
    gram = ObjectProperty()
    comment = ObjectProperty()
    unit = ObjectProperty()

class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (75/255, 0/255, 130/255, .2)
        self.background_down = (75/255, 0/255, 130/255, 1)
        self.background_normal = (75/255, 0/255, 130/255, .2)


class PieceofCake(MDApp, Screen):
    names = ObjectProperty()
    price = ObjectProperty(None)
    quantity = ObjectProperty(None)
    pcs = ObjectProperty(None)
    ml = ObjectProperty(None)
    gram = ObjectProperty(None)
    comment = ObjectProperty(None)
    unit = ObjectProperty()
    search = ObjectProperty()


    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('createIng.kv'))
        screen_manager.add_widget(Builder.load_file('ingredientList.kv'))

        return screen_manager

    def on_start(self):
        pass
        # screen_manager.get_screen('main').date.text = 'Hello'


    def create_ingredient(self, names, price, quantity, pcs, ml, gram, comment, unit):

        now = strftime('%Y-%m-%d %H:%M:%S')
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute(""" INSERT INTO sweet (names,price,quantity,pcs,ml,gram,comment,timeadding) VALUES (?,?,?,?,?,?,?,?)""",
                    (names, price, quantity, pcs, ml, gram, comment, now))
        con.commit()
        con.close()

    def show_comment(self, comment):
        self.comment = comment
        self.dialog = MDDialog(
            title=str(comment), on_touch_down=MDDialog.dismiss, md_bg_color=(72/255, 61/255, 139/255, .9), radius=[20])
        self.dialog.open()


    def clean_ingredient_list(self):
        screen_manager.get_screen('ingredientList').ingredientList.clear_widgets()

    def ingredientList(self):
        screen_manager.get_screen('ingredientList')

    all_ingredients = []
    filtered_ingredients = []

    def search_ingredient(self, search):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet""")
        for x in cur:
            self.all_ingredients.append(x[1])

        for x in self.all_ingredients:
            if search.lower() in x.lower():
                self.filtered_ingredients.append(x)
        print(self.filtered_ingredients)

    def load_ingredient(self):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet ORDER BY timeadding DESC""")
        for x in cur:
            names = x[1]
            price = x[2]
            quantity = x[3]
            pcs = x[4]
            ml = x[5]
            gram = x[6]
            comment = x[7]
            # self.all_ingredients.append(x)

            if pcs == 'down':
                unit = 'pcs'
            elif ml == 'down':
                unit = 'ml'
            elif gram == 'down':
                unit = 'gr'
            else:
                unit = 'NA'

            screen_manager.get_screen('ingredientList').ingredientList.add_widget(AddIngredient(names=names, price=price, quantity=quantity,
                                                                                       pcs=pcs, ml=ml, gram=gram, comment=comment, unit=unit))



# Create the SQL
    con = sql.connect('sweet.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE  IF NOT EXISTS  sweet(
            UserID integer PRIMARY KEY,
            names text,
            price text,
            quantity text,
            pcs state,
            ml state,
            gram state,
            comment text,
            timeadding timestamp)
            """)
    con.commit()
    con.close()


if __name__ == '__main__':
    PieceofCake(). run()