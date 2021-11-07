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
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

Window.size = (360, 770)  # (1080, 2340)

class MainPageRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    Renames = ObjectProperty()
    Diameter = ObjectProperty()
    names = ObjectProperty()
    unit = ObjectProperty()
    qty = ObjectProperty()
    Weight = ObjectProperty()


class CustomPopup(Popup, FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    contentBox = ObjectProperty()
    Renames = ObjectProperty()
    Recomment = ObjectProperty()
    unit = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (75 / 255, 0 / 255, 130 / 255, .6)

    def show_recipe1(self, Renames):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM names WHERE names = '{Renames}'""")

        for x in cur:
            UserID = x[0]
            Renames = x[1]
            Recomment = x[2]
            if Recomment == '':
                Recomment = ' '

        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM ingredients WHERE namesID = '{UserID}'""")

        unit = []
        for y in cur:
            ing_name = y[1]
            unit1 = y[2]
            qty = y[3]

            unitx = ing_name + '  ' + qty + '  ' + unit1
            unit.append(unitx)
            all_units = ('\n'.join(unit))
        self.popup = CustomPopup(title=Renames, title_size='25sp', title_color=[1,1,1, 1], title_font='KaushanScript-Regular.ttf',
                                 unit=all_units, Recomment=Recomment).open()

        con.commit()
        con.close()


class CustomPopupRecipe(Popup, FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    unit = ObjectProperty()



class CompleteRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    Renames = ObjectProperty()
    UnitC = ObjectProperty()
    names = ObjectProperty()
    unit = ObjectProperty()
    qty = ObjectProperty()
    quantity = ObjectProperty()
    Diameter = ObjectProperty()
    Weight = ObjectProperty()



    def on_long_touch(self, *args):
        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .18, 'center_y': .6},
                                                size_hint=(.3, .3),
                                                theme_text_color='Custom',
                                                text_color=(1, 1, 1, 1),
                                                on_release=self.edit_button)
        layout1.add_widget(self.editButton)
        self.deleteButton = MDFillRoundFlatButton(text='Delete', pos_hint={'center_x': .55, 'center_y': .6},
                                                  size_hint=(.3, .3),
                                                  theme_text_color='Custom',
                                                  text_color=(1, 1, 1, 1),
                                                  on_release=self.delete_button)
        layout1.add_widget(self.deleteButton)
        self.closeButton = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .85, 'center_y': .6},
                                                 size_hint=(.1, .3),
                                                 theme_text_color='Custom',
                                                 text_color=(1, 1, 1, 1),
                                                 on_release=self.closeWindow1)
        layout1.add_widget(self.closeButton)
        layout.add_widget(layout1)

        self.pop1 = Popup(title=self.Renames, background_color='white', title_font='KaushanScript-Regular.ttf',
                          content=layout,
                          size_hint=(None, None), size=(600, 300), pos_hint={'center_x': .5, 'center_y': .5})
        self.pop1.open()
        return layout

    def edit_button(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM names""")
        for x in cur:
            self.names_names = x[1]
            if self.Renames == self.names_names:
                self.comment = x[2]

        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editNames = MDTextFieldRect(text=self.Renames, pos=(100, 1000), size_hint=(.95, .07), multiline=False)
        layout1.add_widget(self.editNames)


        self.editComment = MDTextFieldRect(text=self.comment, pos=(100, 600), size_hint=(.95, .3))
        layout1.add_widget(self.editComment)

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .45, 'center_y': .2},
                                                size_hint=(.3, .1),
                                                theme_text_color='Custom',
                                                text_color=(1, 1, 1, 1),
                                                on_release=self.editIngredient)
        layout1.add_widget(self.editButton)

        self.close2Button = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .9, 'center_y': .2},
                                                  size_hint=(.1, .1),
                                                  theme_text_color='Custom',
                                                  text_color=(1, 1, 1, 1),
                                                  on_press=self.closeWindow1,
                                                  on_release=self.closeWindow2)
        layout1.add_widget(self.close2Button)
        layout.add_widget(layout1)

        self.pop2 = Popup(title=self.Renames, background_color='white', title_font='KaushanScript-Regular.ttf',
                          content=layout,
                          size_hint=(None, None), size=(600, 800), pos_hint={'center_x': .5, 'center_y': .5},
                          auto_dismiss=False)
        self.pop2.open()
        return layout



    def delete_button(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM names""")

        for idis in cur:
            self.names_names = idis[1]
            if self.Renames == self.names_names:
                self.delID = idis[0]
                cur.execute("""SELECT * FROM ingredients""")
                cur.execute(f"""DELETE FROM ingredients WHERE namesID = '{self.delID}'""")
        cur.execute(f"""DELETE FROM names WHERE names = '{self.Renames}'""")
        con.commit()
        con.close()
        self.pop1.dismiss()
        self.pieceofcake = PieceofCake()
        self.pieceofcake.clean_ingredient_list()
        self.pieceofcake.load_ingredient()

        self.snackbar = PieceofCake()
        self.snackbar.Snackbar_message(
            message="[color=#ff6600]Ingredient [/color]" + str(self.Renames) + "[color=#ff6600] removed![/color]")
        self.pieceofcake.clean_ingSelector_list()
        self.pieceofcake.load_recipes()


    def editIngredient(self, obj):
        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM names""")
        names = self.Renames
        editNames = self.editNames.text
        editComment = self.editComment.text
        now = strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f""" UPDATE names SET names = '{editNames}',
                                            comment = '{editComment}',
                                            timeadding = '{now}' WHERE names = '{names}'""")
        con.commit()
        con.close()

        self.pop1.dismiss()
        self.pop2.dismiss()
        self.pieceofcake = PieceofCake()
        self.pieceofcake.clean_ingredient_list()
        self.pieceofcake.load_ingredient()
        self.snackbar = PieceofCake()
        self.snackbar.Snackbar_message(
            message="[color=#ff6600]Ingredient [/color]" + str(names) + "[color=#ff6600] edited![/color]")
        self.pieceofcake.clean_ingSelector_list()
        self.pieceofcake.load_recipes()

    def closeWindow1(self, obj):
        self.pop1.dismiss()

    def closeWindow2(self, obj):
        self.pop2.dismiss()


class AddIngToRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    unit = ObjectProperty()
    qty = ObjectProperty()
    Renames = ObjectProperty()



class AddRecipe(FakeRectangularElevationBehavior, FloatLayout, TouchBehavior):
    names = ObjectProperty()
    unit = ObjectProperty()
    qty = ObjectProperty()
    Renames = ObjectProperty()


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
    qty = ObjectProperty()
    Renames = ObjectProperty()

    def on_long_touch(self, *args):
        layout = BoxLayout(orientation='vertical')
        layout1 = FloatLayout()

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .18, 'center_y': .6},
                                                size_hint=(.3, .3),
                                                theme_text_color='Custom',
                                                text_color=(1, 1, 1, 1),
                                                on_release=self.edit_button)
        layout1.add_widget(self.editButton)
        self.deleteButton = MDFillRoundFlatButton(text='Delete', pos_hint={'center_x': .55, 'center_y': .6},
                                                  size_hint=(.3, .3),
                                                  theme_text_color='Custom',
                                                  text_color=(1, 1, 1, 1),
                                                  on_release=self.delete_button)
        layout1.add_widget(self.deleteButton)
        self.closeButton = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .85, 'center_y': .6},
                                                 size_hint=(.1, .3),
                                                 theme_text_color='Custom',
                                                 text_color=(1, 1, 1, 1),
                                                 on_release=self.closeWindow1)
        layout1.add_widget(self.closeButton)
        layout.add_widget(layout1)

        self.pop1 = Popup(title=self.names, background_color='white', title_font='KaushanScript-Regular.ttf',
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

        self.editNames = MDTextFieldRect(text=self.names, background_color=(1,1,1,.9), pos=(100, 1000), size_hint=(.95, .07), multiline=False)
        layout1.add_widget(self.editNames)

        self.editPrice = MDTextFieldRect(text=self.price, background_color=(1,1,1,.9), pos=(100, 920), size_hint=(.45, .07), multiline=False)
        layout1.add_widget(self.editPrice)

        self.editQty = MDTextFieldRect(text=self.quantity, background_color=(1,1,1,.9), pos=(100, 840), size_hint=(.45, .07), multiline=False)
        layout1.add_widget(self.editQty)

        self.editPcs = MyToggleButton(text='Pcs', pos=(350, 840), size_hint=(.09, .07), group='unit')
        self.editMl = MyToggleButton(text='Ml', pos=(450, 840), size_hint=(.09, .07), group='unit')
        self.editGram = MyToggleButton(text='Gr', pos=(550, 840), size_hint=(.09, .07), group='unit')

        self.editComment = MDTextFieldRect(text=self.comment, background_color=(1,1,1,.9), pos=(100, 600), size_hint=(.95, .3))

        layout1.add_widget(self.editPcs)
        layout1.add_widget(self.editMl)
        layout1.add_widget(self.editGram)
        layout1.add_widget(self.editComment)

        self.editButton = MDFillRoundFlatButton(text='Edit', pos_hint={'center_x': .45, 'center_y': .2},
                                                size_hint=(.3, .1),
                                                theme_text_color='Custom',
                                                text_color=(1, 1, 1, 1),
                                                on_release=self.editIngredient)
        layout1.add_widget(self.editButton)

        self.close2Button = MDFillRoundFlatButton(text='X', pos_hint={'center_x': .9, 'center_y': .2},
                                                  size_hint=(.1, .1),
                                                  theme_text_color='Custom',
                                                  text_color=(1, 1, 1, 1),
                                                  on_press=self.closeWindow1,
                                                  on_release=self.closeWindow2)
        layout1.add_widget(self.close2Button)
        layout.add_widget(layout1)

        self.pop2 = Popup(title=self.names, background_color=(1, 1, 1, 1), title_font='KaushanScript-Regular.ttf',
                          content=layout,
                          size_hint=(None, None), size=(600, 800), pos_hint={'center_x': .5, 'center_y': .5},
                          auto_dismiss=False)
        self.pop2.open()
        return layout

    all_ing_names = []
    all_recipe_names = []
    all_IDs = []
    def delete_button(self, obj):

        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM ingredients""")
        for x in cur:
            ing_names = x[1]
            namesID = x[4]
            self.all_ing_names.append(ing_names)
            if self.names in self.all_ing_names and self.names == ing_names:

                con = sql.connect('sweet.db')
                cur = con.cursor()
                cur.execute("""SELECT * FROM names""")
                for y in cur:
                    recipe_name = y[1]
                    recipeID = y[0]
                    self.all_IDs.append(recipeID)
                    if namesID in self.all_IDs and namesID == recipeID:
                        self.all_recipe_names.append(recipe_name)
                # print(str(self.names) + str(namesID))

        list_of_recipes = ('\n'.join(self.all_recipe_names))

        if list_of_recipes:
            self.popup = CustomPopupRecipe(title="Can't delete: "+self.names, title_size='25sp', title_color=[200 / 255, 199 / 255, 234 / 255, 1],title_font='KaushanScript-Regular.ttf',
                                     unit=list_of_recipes).open()

            self.all_ing_names.clear()
            self.all_recipe_names.clear()
            self.all_IDs.clear()
        else:
            con = sql.connect('sweet.db')
            cur = con.cursor()
            cur.execute("""SELECT * FROM sweet""")
            cur.execute("""DELETE FROM sweet WHERE names = ? and price = ? and quantity = ? and comment = ?""",
                        (self.names, self.price, self.quantity, self.comment))
            con.commit()

            self.pop1.dismiss()
            self.pieceofcake = PieceofCake()
            self.pieceofcake.clean_ingredient_list()
            self.pieceofcake.load_ingredient()

            self.snackbar = PieceofCake()
            self.snackbar.Snackbar_message(
                message="[color=#ff6600]Ingredient [/color]" + str(self.names) + "[color=#ff6600] removed![/color]")

    def close_clear(self):
        self.all_ing_names.clear()
        self.all_recipe_names.clear()
        self.all_IDs.clear()

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

        self.snackbar = PieceofCake()
        self.snackbar.Snackbar_message(
            message="[color=#ff6600]Ingredient [/color]" + str(self.names) + "[color=#ff6600] edited![/color]")


    def closeWindow1(self, obj):
        self.pop1.dismiss()

    def closeWindow2(self, obj):
        self.pop2.dismiss()


class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (75 / 255, 0 / 255, 130 / 255, .3)
        self.background_down = (75 / 255, 0 / 255, 130 / 255, .8)
        self.background_normal = (75 / 255, 0 / 255, 130 / 255, .3)


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
    addRemove = ObjectProperty()
    qty = ObjectProperty()
    Renames = ObjectProperty()
    Recomment = ObjectProperty()
    unitC = ObjectProperty()
    spinner_cake = ObjectProperty()
    weight = ObjectProperty()
    square = ObjectProperty()
    circle = ObjectProperty()

    popup = None

    def Snackbar_message(self, message):
        Snackbar(text=f'[font=KaushanScript-Regular.ttf]{message}[/font]',
                 snackbar_x='10dp', snackbar_y='10dp',
                 duration=1,
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                 bg_color=(75 / 255, 0 / 255, 130 / 255, .2),
                 radius=[20],
                 font_size='20sp').open()

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file('main.kv'))
        screen_manager.add_widget(Builder.load_file('createIng.kv'))
        screen_manager.add_widget(Builder.load_file('ingredientList.kv'))
        screen_manager.add_widget(Builder.load_file('createRecipe.kv'))
        screen_manager.add_widget(Builder.load_file('ingSelector.kv'))
        screen_manager.add_widget(Builder.load_file('recipeList.kv'))

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
            cur.execute(
                """ INSERT INTO sweet (names,price,quantity,pcs,ml,gram,comment,timeadding) VALUES (?,?,?,?,?,?,?,?)""",
                (names, price, quantity, pcs, ml, gram, comment, now))
            con.commit()
            con.close()
        else:
            self.Snackbar_message(message="[color=#ff6600]Ingredient [/color]" + str(names) + "[color=#ff6600] is already exists![/color]")


    def show_comment(self, comment):
        self.comment = comment
        self.dialog = MDDialog(
            title=str(comment), on_touch_down=MDDialog.dismiss, md_bg_color=(72 / 255, 61 / 255, 139 / 255, .9),
            radius=[20])
        self.dialog.open()

    def clean_ingredient_list(self):
        screen_manager.get_screen('ingredientList').ingredientList.clear_widgets()

    def clean_ingSelector_list(self):
        screen_manager.get_screen('recipeList').recipeList.clear_widgets()

    def filter_ingredients(self, ingredients, message):
        if message == '':
            return ingredients

        filteredIngredients = []

        for x in ingredients:
            if message.lower() in x[1].lower():
                filteredIngredients.append(x)

        return filteredIngredients

    def load_ingredient(self, search=''):
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

            screen_manager.get_screen('ingredientList').ingredientList.add_widget(
                AddIngredient(names=names, price=price, quantity=quantity,
                              ml=ml, gram=gram, comment=comment, unit=unit))

    def add_ingredient_to_recipe(self, search=''):
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

    all_names = []
    all_qtys = []
    all_units = []
    nameID = []

    def add_ing_to_recipe(self, names, unit, qty):
        screen_manager.get_screen('createRecipe').ingredientforRecipe.add_widget(
            AddIngToRecipe(names=names, unit=qty + ' ' + unit))

        self.all_names.append(names)
        self.all_qtys.append(qty)
        self.all_units.append(unit)
        self.names = self.all_names
        self.qty = self.all_qtys
        self.unit = self.all_units

    def create_recipe(self, Renames, Recomment, Weight, Diameter):
        try:
            con = sql.connect('sweet.db')
            cur = con.cursor()
            cur.execute(f"SELECT names FROM names WHERE names = '{Renames}'")
            if cur.fetchone() is None:
                now = strftime('%Y-%m-%d %H:%M:%S')
                con = sql.connect('sweet.db')
                cur = con.cursor()
                cur.execute(
                    """ INSERT INTO names (names,comment,diameter,unit,timeadding) VALUES (?,?,?,?,?)""",
                    (Renames, Recomment, Diameter, Weight, now))
                con.commit()
                # con.close()

                con = sql.connect('sweet.db')
                cur = con.cursor()
                cur.execute(f"SELECT UserID FROM names WHERE names = '{Renames}'")

                m = cur.fetchone()[0]
                for i in range(len(self.names)):
                    self.nameID.append(m)
                    self.nameIDs = self.nameID

                con = sql.connect('sweet.db')
                cur = con.cursor()
                cur.executemany(""" INSERT INTO ingredients (ing_names, unit, quantity, namesID) VALUES (?,?,?,?)""",
                                zip(self.names, self.unit, self.qty, self.nameID))
                con.commit()
                con.close()

            else:
                self.Snackbar_message(message="[color=#ff6600]Ingredient [/color]" + str(
                    Renames) + "[color=#ff6600] is already exists![/color]")

        except:
            self.Snackbar_message(message="[color=#ff6600]    Add at least one ingredient![/color]")

    def delete_ing(self):
        self.nameIDs.clear()
        self.all_names.clear()
        self.all_qtys.clear()
        self.all_units.clear()

    def load_recipes(self):

        con = sql.connect('sweet.db')
        cur = con.cursor()
        cur.execute("""SELECT * FROM names ORDER BY names ASC""")

        for x in cur:
            Renames = x[1]
            Diameter = x[3]
            Weight = x[4]
            screen_manager.get_screen('recipeList').recipeList.add_widget(CompleteRecipe(Renames=Renames, Diameter=Diameter, Weight=Weight))
        con.close()

    def show_recipe(self, Renames):
        custom_popup = CustomPopup()
        show_rec = custom_popup.show_recipe1(Renames)
        # print(show_rec)

    all_mainpages_names = []
    all_diameteres = []

    def add_ing_to_mainpage(self, Renames, Diameter, Weight):
        screen_manager.get_screen('main').main_page.add_widget(MainPageRecipe(Renames=Renames, Diameter=Diameter, Weight=Weight))

        self.all_mainpages_names.append(Renames)
        self.mainpages_names = self.all_mainpages_names

        self.all_diameteres.append(Diameter)
        self.diameteres = self.all_diameteres
        # print(max(self.diameteres))
        self.max_diameter = max(self.diameteres)

    def remove_ing_from_main_page(self, Renames, Weight, Diameter):
        self.mainpages_names.remove(Renames)
        diameter = ''.join(map(str, [int(word) for word in Diameter.split() if word.isdigit()]))
        self.diameteres.remove(diameter)


    def coefficient(self, square, circle, square_length, square_width, circle_diameter):
        self.coeff = 0
        if square == 'down':
            if square_length != '' and square_width != '':
                self.coeff = round((((float(square_length)) *
                                      (float(square_width))) / ((((float(self.max_diameter)) / 2) *
                                       ((float(self.max_diameter)) / 2)) * 3.1415)), 4)
            else:
                self.Snackbar_message(message="[color=#ff6600]    Empty Fields![/color]")

        elif circle == 'down':
            if circle_diameter != '':
                self.coeff = round(float(circle_diameter) *
                                        (float(circle_diameter)) /
                                        (float(self.max_diameter) * (float(self.max_diameter))), 4)
            else:
                self.Snackbar_message(message="[color=#ff6600]    Empty Fields![/color]")
        else:
            self.coeff = 1

    one_ing_final_price = []
    def result_price(self):
        print('Koefficient '+str(self.coeff)+'\n')
        try:
            self.weight = 0
            self.final_price = 0
            User = []
            ing_names = []
            for ing in self.mainpages_names:
                con = sql.connect('sweet.db')
                cur = con.cursor()
                cur.execute(f"SELECT * FROM names WHERE names = '{ing}'")
                for x in cur:
                    UserID = x[0]
                    weight = x[4]
                    diameter = x[3]
                    User.append(UserID)
                    print(ing+' '+weight+'Gr '+diameter+'Cm ')
                    self.weight = int(self.weight + int(weight) * self.coeff)
                    print('weight = ' + str(self.weight))

                    for y in User:
                        con = sql.connect('sweet.db')
                        cur = con.cursor()
                        cur.execute(f"SELECT * FROM ingredients WHERE namesID = '{y}'")
                        for z in cur:
                            ing_name = z[1]
                            ing_qty = z[3]
                            ing_names.append(ing_name)
                            self.ing_qty_coeff = float(ing_qty) * float(self.coeff)
                            print('   '+ing_name+' '+str(self.ing_qty_coeff)+' qty')
                            User.clear()
    #Price
                            for b_i in ing_names:
                                con = sql.connect('sweet.db')
                                cur = con.cursor()
                                cur.execute(f"SELECT * FROM sweet WHERE names = '{b_i}'")
                                for i in cur:
                                    basic_ing_name = i[1]
                                    basic_ing_price = i[2]
                                    basic_ing_qty = i[3]

                                    self.ing_final_price = float(self.ing_qty_coeff) * float(basic_ing_price)/float(basic_ing_qty)
                                    # different = self.final_price - self.ing_final_price

                            self.final_price = round((self.final_price + self.ing_final_price), 2)

                            print(str(basic_ing_name) + ' basic price = ' + str(basic_ing_price) + '$' + ' --> ' + str(basic_ing_qty + ' Gr'))

            print('\n')

            print(self.final_price)

        except:
            self.Snackbar_message(message="[color=#ff6600]    Add at least one ingredient![/color]")

    def save_as(self, weight, save_as):
        h = 500

        pdfmetrics.registerFont(TTFont('KaushanScript-Regular', 'KaushanScript-Regular.ttf'))
        pdf_name = str(save_as) + '.pdf'
        canvas = Canvas(pdf_name, pagesize=(180, 510))
        canvas.setFillColor('#4B0082')


        recipe_to_pdf = []
        diam_to_pdf = []
        weight_to_pdf = []
        for part_of_recipe_name in self.all_mainpages_names:
            con = sql.connect('sweet.db')
            cur = con.cursor()
            cur.execute(f"SELECT * FROM names WHERE names = '{part_of_recipe_name}'")
            for x in cur:
                h = h-12
                canvas.setFont('KaushanScript-Regular', 12)
                recipe_id = x[0]
                diam = x[3]
                weight = x[4]
                names_diam_weight = (part_of_recipe_name+' D='+diam+' W='+weight+':')
                print(names_diam_weight)
                canvas.drawString(10, h, str(names_diam_weight))
                h=h-3
                canvas.line(10,h, 170, h)
                cur.execute(f"SELECT * FROM ingredients WHERE namesID = '{recipe_id}'")

                for z in cur:
                    h = h - 12
                    canvas.setFont('KaushanScript-Regular', 8)
                    ing_name = z[1]
                    ing_qty = z[3]
                    ing_unit = z[2]
                    ing_names_qty_unit = (ing_name+' '+ing_qty+' '+ing_unit)
                    print(ing_names_qty_unit)
                    canvas.drawString(10, h, ing_names_qty_unit)
                recipe_to_pdf.append(part_of_recipe_name)
                diam_to_pdf.append(diam)
                weight_to_pdf.append(weight)
            h = h - 8
        print('\nTotal price = '+str(self.final_price))
        print(recipe_to_pdf)
        h=h-20
        print(h)
        if h < 0:
            h = h+370
        canvas.setFont('KaushanScript-Regular', 14)
        final_price_to_pdf = ('Total price: '+str(self.final_price))
        canvas.drawString(10, h, str(final_price_to_pdf))


        # if not os.path.exists(f"recipes/'{save_as}'.pdf"):
        #     os.mkdir(f"recipes/'{save_as}'.pdf")
        canvas.save()

    # Create the SQL
    con = sql.connect('sweet.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE  IF NOT EXISTS  sweet(
            UserID integer PRIMARY KEY AUTOINCREMENT,
            names text,
            price text,
            quantity text,
            pcs state,
            ml state,
            gram state,
            comment text,
            timeadding timestamp)
            """)
    cur.execute("""CREATE TABLE  IF NOT EXISTS  names(
                UserID integer PRIMARY KEY AUTOINCREMENT,
                names text,
                comment text,
                diameter text,
                unit text,
                timeadding timestamp)
                """)
    cur.execute("""CREATE TABLE  IF NOT EXISTS  ingredients(
                UserID integer PRIMARY KEY AUTOINCREMENT,
                ing_names text,
                unit text,
                quantity text,
                namesID integer,
                FOREIGN KEY(namesID) REFERENCES names(namesID))
                """)
    con.commit()
    con.close()


if __name__ == '__main__':
    PieceofCake().run()
