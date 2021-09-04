from time import strftime
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
import sqlite3 as sql
from kivy.metrics import dp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors import TouchBehavior
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
Window.size = (360, 770)  #(1080, 2340)


class AddIngredient(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    price = ObjectProperty()
    quantity = ObjectProperty()
    pcs = ObjectProperty()
    ml = ObjectProperty()
    gram = ObjectProperty()
    comment = ObjectProperty()
    unit = ObjectProperty()

    def on_long_touch(self, *args):
        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .18, 'center_y': .6}, size_hint=(.3, .3),
                                                 theme_text_color='Custom',
                                                 text_color=(0, 1, 0, 1),
                                                 on_release=self.edit_button)
        layout1.add_widget(self.editButton)
        self.deleteButton = MDFillRoundFlatButton(text='Delete', pos_hint={'center_x': .55, 'center_y': .6},
                                                size_hint=(.3, .3),
                                                theme_text_color='Custom',
                                                text_color=(0, 1, 0, 1),
                                                on_release=self.delete_button)
        layout1.add_widget(self.deleteButton)
        self.closeButton = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .85, 'center_y': .6},
                                                  size_hint=(.1, .3),
                                                  theme_text_color='Custom',
                                                  text_color=(0, 1, 0, 1),
                                                  on_release=self.closeWindow)
        layout1.add_widget(self.closeButton)
        layout.add_widget(layout1)

        self.pop = Popup(title=self.names, background_color='white',
                         content=layout,
                         size_hint=(None, None), size=(600, 300), pos_hint={'center_x': .5, 'center_y': .5})
        self.pop.open()
        return layout

    def edit_button(self, obj):
        screen_manager.current = 'maining'
        print('Edit')
        self.pop.dismiss()

    def delete_button(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet""")
        delete = """DELETE FROM sweet WHERE names = ?"""
        cur.execute(delete, (self.names,))
        con.commit()

        self.pop.dismiss()
        self.pieceofcake = PieceofCake()
        self.pieceofcake.clean_ingredient_list()
        self.pieceofcake.load_ingredient()

        Snackbar(text="[color=#ff6600]Ingredient [/color]" + str(self.names) + "[color=#ff6600] removed![/color]",
                 snackbar_x='10dp', snackbar_y='10dp',
                 duration=1,
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                 bg_color=(75 / 255, 0 / 255, 130 / 255, .2),
                 radius=[20],
                 font_size='17sp').open()


    def closeWindow(self, obj):
        self.pop.dismiss()

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
    message = ObjectProperty()
    create_ingredient = ObjectProperty()


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

    # def ingredientList(self):
    #     screen_manager.get_screen('ingredientList')

    # def toCreateWindow(self):
    #     self.screen_manager.get_screen('main')



    def filter_ingredients(self, ingredients, message):
        if message == '':
            return ingredients

        filteredIngredients = []

        for x in ingredients:
            if message.lower() in x[1].lower():
                filteredIngredients.append(x)

        return filteredIngredients

    def load_ingredient(self, search = ''):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet ORDER BY timeadding DESC""")

        toFilter = []
        for x in cur:
            toFilter.append(x)

        filteredIngredients = self.filter_ingredients(toFilter, search)

        screen_manager.get_screen('ingredientList').ingredientList.clear_widgets()
        for x in filteredIngredients:
            names = x[1]
            price = x[2]
            quantity = x[3]
            pcs = x[4]
            ml = x[5]
            gram = x[6]
            comment = x[7]

            if pcs == 'down':
                unit = 'pcs'
            elif ml == 'down':
                unit = 'ml'
            elif gram == 'down':
                unit = 'gr'
            else:
                unit = 'NA'

            screen_manager.get_screen('ingredientList').ingredientList.add_widget(AddIngredient(names=names, price=price, quantity=quantity,
                                                                                                ml=ml, gram=gram, comment=comment, unit=unit))


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