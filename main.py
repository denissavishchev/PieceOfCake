from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
import sqlite3 as sql
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import FloatLayout
from kivy.core.window import Window
Window.size = (360, 770)  #(1080, 2340)


class AddIngredient(FakeRectangularElevationBehavior, FloatLayout):
    names = StringProperty()
    price = StringProperty()
    quantity = StringProperty()
    pcs = StringProperty()
    ml = StringProperty()
    gr = StringProperty()
    comment = StringProperty()




class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (75/255, 0/255, 130/255, .2)
        self.background_down = (75/255, 0/255, 130/255, 1)
        self.background_normal = (75/255, 0/255, 130/255, .2)


class PieceofCake(MDApp, Screen):
    names = ObjectProperty(None)
    price = ObjectProperty(None)
    quantity = ObjectProperty(None)
    pcs = ObjectProperty(None)
    ml = ObjectProperty(None)
    gram = ObjectProperty(None)
    comment = ObjectProperty(None)

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

    def on_complete(self, checkbox, value, description, bar):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179/255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170/255, 23/255, 1

    def create_ingredient(self, names, price, quantity):
        screen_manager.get_screen('ingredientList').ingredientList.add_widget(AddIngredient(names=names, price=price, quantity=quantity))


    def add_ingredient_to_base(self):

        # names = self.names.text
        # price = self.price.text
        # quantity = self.quantity.text
        # pcs = self.pcs.state
        # ml = self.ml.state
        # gram = self.gr.state
        # comment = self.comment.text

        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute(""" INSERT INTO sweet (names,price,quantity,pcs,ml,gram,comment) VALUES (?,?,?,?,?,?,?)""",
                    (self.names.text, self.price.text, self.quantity.text, self.pcs.state, self.ml.state,
                     self.gram.state, self.comment.text))
        con.commit()
        con.close()

    def ingredientList(self):
        screen_manager.get_screen('ingredientList')

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
            comment text)
            """)
    con.commit()
    con.close()


if __name__ == '__main__':
    PieceofCake(). run()