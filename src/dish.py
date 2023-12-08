import connection_manager as db
from queries import queries


class DishManager:
    def __init__(self):
        self.dishes = get_names("dish")
        self.ingredients = get_names("ingredient")
        self.origins = get_names("origin")
        self.categories = ["all categories", *get_names("category")]
        self.dish_details: dict[str, dict] = {dish_name: get_dish_details(dish_name) for dish_name in self.dishes}
        self.ingredient_details: dict[str, dict] = {ingredient_name: get_ingredient_details(ingredient_name)[0]
                                                    for ingredient_name in self.ingredients}

    def get_dish_details(self, dish_name):
        return self.dish_details[dish_name]

    def get_ingredient_details(self, ingredient_name):
        return self.ingredient_details[ingredient_name]

    def get_ingredients_details(self, ingredients):
        return zip(ingredients, [self.get_ingredient_details(name) for name in ingredients])


def get_names(table_name):
    query = f"SELECT name FROM {table_name}"
    return [i["name"] for i in db.execute_query(query)]


def get_id(item_name, table_name):
    return db.execute_query(f"SELECT id FROM {table_name} WHERE name=%s", (item_name,))[0]["id"]


def get_dish_origin(dish_id):
    return db.execute_query(queries["origin"], (dish_id,))


def get_dish_category(dish_id):
    return db.execute_query(queries["category"], (dish_id,))


def get_dish_ingredients_name(dish_id):
    return db.execute_query(queries["dish_ingredient"], (dish_id,))


def get_ingredient_details(ingredient_name):
    return db.execute_query(queries["ingredient_details"], (ingredient_name,))


def get_dish_price(dish_id):
    return db.execute_query(queries["price"], (dish_id,))


def get_serving_hours(dish_id):
    return db.execute_query(queries["serving_hours"], (dish_id,))


def get_dish_details(dish_name):
    dish_id = get_id(dish_name, "dish")
    price = get_dish_price(dish_id)
    origins = get_dish_origin(dish_id)
    category = get_dish_category(dish_id)
    ingredients = get_dish_ingredients_name(dish_id)
    return {
        "name": dish_name,
        "price": price[0]["price"],
        "serving hours": "",
        "origin": [i["name"] for i in origins],
        "category": category[0]["name"],
        "ingredients": [i["name"] for i in ingredients],
    }


def get_dishes(category, origin, show_unavailable):
    query = "SELECT id FROM dish" if show_unavailable else queries["available_dish"]

    if category:
        category_id = get_id(category, "category")
        category_filter = f"SELECT dish.id FROM dish WHERE category_id={category_id}"
        query += f" INTERSECT ({category_filter})"

    if origin:
        origin_ids = [get_id(o, "origin") for o in origin]
        origin_filter = f"""
        select dish.id
        from dish
        inner join dish_origin on dish.id=dish_id
        where origin_id in ({','.join(str(id) for id in origin_ids)})
        group by dish.id
        having count(origin_id)={len(origin_ids)}
        """
        query += f" INTERSECT ({origin_filter})"

    result = f"SELECT name FROM dish WHERE id IN ({query})"
    return [dish['name'] for dish in db.execute_query(result)]
