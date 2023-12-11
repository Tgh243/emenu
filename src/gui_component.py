from dearpygui import dearpygui as dpg
import dpg_util as dpg_util

HELP_TOOLTIP = """
Filter usage:\n
""         display all lines\n
"xxx"      display lines containing "xxx"\n
"xxx,yyy"  display lines containing "xxx" or "yyy"\n
"-xxx"     hide lines containing "xxx

"""


def display_dish_details(parent, dish_name, dish_manager):
    dish_details = dish_manager.get_dish_details(dish_name)
    dpg.add_text(f"Dish Name: {dish_details['name']}", parent=parent)
    dpg.add_text(f"Price: {dish_details['price']}$", parent=parent)
    dpg.add_text(f"Origin: {', '.join(dish_details['origins'])}", parent=parent)
    dpg.add_text(f"Category: {dish_details['category']}", parent=parent)
    dpg.add_text("Ingredients:", parent=parent)

    for ingredient_name, details in dish_manager.get_ingredients_details(dish_details["ingredients"]):
        item = dpg.add_text(f"{ingredient_name}", indent=20, bullet=True, parent=parent)
        with dpg.tooltip(parent=item):
            dpg.add_text(f"Quantity: {details['quantity']:.0f} {details['unit']}")
            dpg.add_text(f"Import Date: {details['import_date']}")
            dpg.add_text(f"Expired Date: {details['expired_date']}")


def create_search_interface():
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="search_box", hint="search for a dishes", width=350,
                           callback=lambda: dpg.set_value("filter_id", dpg.get_value("search_box")))
        dpg.add_button(tag="apply_button", label="apply", show=False)
        dpg.configure_item("apply_button", height=dpg.get_item_height("search_box"))
        dpg.configure_item("apply_button", width=len(dpg.get_item_label("apply_button")) * 10)
        dpg_util.help_tooltip(HELP_TOOLTIP)


def create_filter_popup(apply_filter_callback, categories: list, origins: list):
    cat_length = len(max(categories, key=len))
    button = dpg.add_button(label="filters", width=70)

    def clear_filter():
        for o in origins:
            dpg.set_value(o, False)
        dpg.set_value(item="categories", value=categories[0])

    with dpg.popup(mousebutton=dpg.mvMouseButton_Left, parent=button):
        menu1 = dpg.add_menu(label="categories", tag="category_filter")
        menu2 = dpg.add_menu(label="origins", tag="origin_filter")

        dpg.add_checkbox(tag="availability", default_value=True, label="show unavailable")
        with dpg.group(horizontal=True):
            dpg.add_button(tag="apply_filter", label="apply filter", callback=apply_filter_callback)
            dpg.add_spacer()
            dpg.add_button(tag="clear_filter", label="clear filter", callback=clear_filter)

    dpg.add_combo(tag="categories", default_value=categories[0], width=cat_length * 10, items=categories, parent=menu1)
    for i in origins:
        dpg.add_checkbox(tag=i, label=i, default_value=False, parent=menu2)


def get_filter_values():
    category = dpg.get_value("categories")
    if category == "all categories":
        category = None
    availability = dpg.get_value("availability")
    origin = [
        dpg.get_item_label(child)
        for child in dpg.get_item_children("origin_filter", 1)
        if dpg.get_value(child)
    ]
    return category, origin, availability
