import sqlite3 as sql
from time import strftime

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextFieldRect


Window.size = (360, 770)  #(1080, 2340)

class AddIngToRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    unit = ObjectProperty()

class AddRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    unit = ObjectProperty()

class AddIngredient(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    price = ObjectProperty()
    quantity = ObjectProperty()
    pcs = ObjectProperty()
    ml = ObjectProperty()
    gram = ObjectProperty()
    comment = ObjectProperty()
    unit = ObjectProperty()
    edit_names = ObjectProperty()
    edit_price = ObjectProperty()
    edit_quantity = ObjectProperty()
    edit_pcs = ObjectProperty()
    edit_ml = ObjectProperty()
    edit_gram = ObjectProperty()
    edit_comment = ObjectProperty()
    namesA = ObjectProperty()

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
                                                  on_release=self.closeWindow1)
        layout1.add_widget(self.closeButton)
        layout.add_widget(layout1)

        self.pop1 = Popup(title=self.names, background_color='white',
                         content=layout,
                         size_hint=(None, None), size=(600, 300), pos_hint={'center_x': .5, 'center_y': .5})
        self.pop1.open()
        return layout

    def edit_button(self, obj):
        # con = sql.connect('sweet.db')
        # cur = con.cursor()
        # cur.execute("""SELECT * FROM sweet""")
        # for x in cur:
        #     pcs = x[4]
        #     ml = x[5]
        #     gram = x[6]

        # if self.pcs == 'down':
        #     self.editPcs.state ='down'
        # elif self.ml == 'down':
        #     self.editMl.state ='down'
        # elif self.gram == 'down':
        #     self.editGram.state ='down'
        # else:
        #     self.unit = 'NA'
        # print(self.unit)

        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editNames = MDTextFieldRect(text=self.names, pos=(100, 1000), size_hint=(.95, .07), multiline=False)
        layout1.add_widget(self.editNames)

        self.editPrice = MDTextFieldRect(text=self.price, pos=(100, 920), size_hint=(.45, .07), multiline=False)
        layout1.add_widget(self.editPrice)

        self.editQty = MDTextFieldRect(text=self.quantity, pos=(100, 840), size_hint=(.45, .07), multiline=False)
        layout1.add_widget(self.editQty)

        self.editPcs = MyToggleButton(text='Pcs', pos=(350, 840), size_hint=(.09, .07), group='unit')
        self.editMl = MyToggleButton(text='Ml', pos=(450, 840), size_hint=(.09, .07), group='unit')
        self.editGram = MyToggleButton(text='Gr', pos=(550, 840), size_hint=(.09, .07), group='unit')

        self.editComment = MDTextFieldRect(text=self.comment, pos=(100, 600), size_hint=(.95, .3))

        layout1.add_widget(self.editPcs)
        layout1.add_widget(self.editMl)
        layout1.add_widget(self.editGram)
        layout1.add_widget(self.editComment)

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .45, 'center_y': .2},
                                                 size_hint=(.3, .1),
                                                 theme_text_color='Custom',
                                                 text_color=(0, 1, 0, 1),
                                                 on_release=self.editIngredient)
        layout1.add_widget(self.editButton)

        self.close2Button = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .9, 'center_y': .2},
                                                size_hint=(.1, .1),
                                                theme_text_color='Custom',
                                                text_color=(0, 1, 0, 1),
                                                on_press=self.closeWindow1,
                                                on_release=self.closeWindow2)
        layout1.add_widget(self.close2Button)
        layout.add_widget(layout1)

        self.pop2 = Popup(title=self.names, background_color='white',
                         content=layout,
                         size_hint=(None, None), size=(600, 800), pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.pop2.open()
        return layout



    def delete_button(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet""")
        cur.execute("""DELETE FROM sweet WHERE names = ? and price = ? and quantity = ? and comment = ?""", (self.names, self.price, self.quantity, self.comment))
        con.commit()

        self.pop1.dismiss()
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

    def editIngredient(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet""")
        names = self.names
        now = strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f""" UPDATE sweet SET names = '{self.editNames.text}',
                                            price = '{self.editPrice.text}',
                                            quantity = '{self.editQty.text}',
                                            pcs = '{self.editPcs.state}',
                                            ml = '{self.editMl.state}',
                                            gram = '{self.editGram.state}',
                                            comment = '{self.editComment.text}',
                                            timeadding = '{now}' WHERE names = '{names}'""")
        con.commit()
        con.close()

        self.pop1.dismiss()
        self.pop2.dismiss()
        self.pieceofcake = PieceofCake()
        self.pieceofcake.clean_ingredient_list()
        self.pieceofcake.load_ingredient()

        Snackbar(text="[color=#ff6600]Ingredient [/color]" + str(self.names) + "[color=#ff6600] edited![/color]",
                 snackbar_x='10dp', snackbar_y='10dp',
                 duration=1,
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                 bg_color=(75 / 255, 0 / 255, 130 / 255, .2),
                 radius=[20],
                 font_size='17sp').open()

    def closeWindow1(self, obj):
        self.pop1.dismiss()
    def closeWindow2(self, obj):
        self.pop2.dismiss()

class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (75/255, 0/255, 130/255, .2)
        self.background_down = (255/255, 102/255, 0/255, 1)
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
    addRemove  =ObjectProperty()


    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('createIng.kv'))
        screen_manager.add_widget(Builder.load_file('ingredientList.kv'))
        screen_manager.add_widget(Builder.load_file('createRecipe.kv'))
        screen_manager.add_widget(Builder.load_file('ingSelector.kv'))

        return screen_manager

    def on_start(self):
        pass
        # screen_manager.get_screen('main').date.text = 'Hello'


    def create_ingredient(self, names, price, quantity, pcs, ml, gram, comment, unit):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute(f"SELECT names FROM sweet WHERE names = '{names}'")
        if cur.fetchone() is None:
            now = strftime('%Y-%m-%d %H:%M:%S')
            con = sql.connect('sweet.db')
            cur = con.cursor()
            cur.execute(""" INSERT INTO sweet (names,price,quantity,pcs,ml,gram,comment,timeadding) VALUES (?,?,?,?,?,?,?,?)""",
                        (names, price, quantity, pcs, ml, gram, comment, now))
            con.commit()
            con.close()
        else:
            Snackbar(text="[color=#ff6600]Ingredient [/color]" + str(names) + "[color=#ff6600] is already exists![/color]",
                     snackbar_x='10dp', snackbar_y='10dp',
                     duration=1,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(75 / 255, 0 / 255, 130 / 255, .2),
                     radius=[20],
                     font_size='17sp').open()


    def show_comment(self, comment):
        self.comment = comment
        self.dialog = MDDialog(
            title=str(comment), on_touch_down=MDDialog.dismiss, md_bg_color=(72/255, 61/255, 139/255, .9), radius=[20])
        self.dialog.open()


    def clean_ingredient_list(self):
        screen_manager.get_screen('ingredientList').ingredientList.clear_widgets()

    def clean_ingSelector_list(self):
        screen_manager.get_screen('ingSelector').selectorList.clear_widgets()


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
    def add_ingredient_to_recipe(self, search = ''):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM sweet ORDER BY names ASC""")

        toFilter = []
        for x in cur:
            toFilter.append(x)

        filteredIngredients = self.filter_ingredients(toFilter, search)

        screen_manager.get_screen('ingSelector').selectorList.clear_widgets()
        for x in filteredIngredients:
            names = x[1]
            pcs = x[4]
            ml = x[5]
            gram = x[6]

            if pcs == 'down':
                unit = 'pcs'
            elif ml == 'down':
                unit = 'ml'
            elif gram == 'down':
                unit = 'gr'
            else:
                unit = 'NA'

            screen_manager.get_screen('ingSelector').selectorList.add_widget(AddRecipe(names=names, unit=unit))

    def add_ing_to_recipe(self, names, unit):
        screen_manager.get_screen('createRecipe').ingredientforRecipe.add_widget(AddIngToRecipe(names=names, unit=unit))


    # def remove_ing_from_recipe(self):
    #     print('Buy')

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