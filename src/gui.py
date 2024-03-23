import dearpygui.dearpygui as dpg
import dish
import dpg_util as dpg_util
from gui_component import (
    display_dish_details,
    create_search_interface,
    create_filter_popup,
    get_filter_values
)


class Gui:
    def __init__(self):
        self.dish_manager = dish.DishManager()
        self.current_dishes = self.dish_manager.dishes

    def run(self):
        with dpg.window(no_collapse=True, no_close=True, no_title_bar=True, min_size=(500, 500), tag="main_window"):
            with dpg.menu_bar():
                dpg_util.add_tools()

            create_search_interface()
            dpg.add_spacer()
            create_filter_popup(self.on_apply_filter, self.dish_manager.categories, self.dish_manager.origins)
            dpg.add_spacer()

            with dpg.child_window():
                with dpg.group(horizontal=True):

                    with dpg.child_window(width=dpg.get_item_width("search_box") * 0.8):
                        with dpg.filter_set(tag="filter_id"):
                            for d in self.dish_manager.dishes:
                                dpg.add_selectable(label=d, filter_key=d, tag=d,
                                                   callback=self.on_select)

                    with dpg.child_window(tag="output_window", horizontal_scrollbar=True):
                        pass

    def on_select(self, sender, app_data):
        if not app_data:
            return
        for i in self.current_dishes:
            if i != sender:
                dpg.set_value(i, False)
        dpg.delete_item("output_window", children_only=True)
        display_dish_details("output_window", sender, self.dish_manager)

    def on_apply_filter(self):
        with dpg.mutex():
            dpg.delete_item("filter_id", children_only=True)
            self.current_dishes = dish.get_dishes_name(*get_filter_values())
            for d in self.current_dishes:
                dpg.add_selectable(label=d, filter_key=d, parent="filter_id", tag=d,
                                   callback=self.on_select)
