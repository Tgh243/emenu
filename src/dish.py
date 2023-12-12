import connection_manager as db
from queries import queries


class DishManager:
    def __init__(self):
        self.dishes = get_names("dish")
        self.ingredients = get_names("ingredient")
        self.origins = get_names("origin")
        self.categories = ["all categories", *get_names("category")]
        self.dish_details = get_dishes_details()
        self.ingredient_details = get_ingredients_details()

    def get_dish_details(self, dish_name) -> dict:
        return self.dish_details[dish_name]

    def get_ingredient_details(self, ingredient_name) -> dict:
        return self.ingredient_details[ingredient_name]

    def get_ingredients_details(self, ingredients) -> dict:
        return zip(ingredients, [self.get_ingredient_details(name) for name in ingredients])


def get_names(table_name):
    query = f"SELECT name FROM {table_name}"
    return [row["name"] for row in db.execute_query(query)]


def get_id(item_name, table_name):
    return db.execute_query(f"SELECT id FROM {table_name} WHERE name=%s", (item_name,))[0]["id"]


def get_dishes_details():
    query = queries['dishes_details'].format(origins=queries['origins'], ingredients=queries['ingredients'])
    return {
        row['name']: {
            'name': row['name'],
            'price': row['price'],
            'category': row['category'],
            'origins': row['origins'].split(','),
            'ingredients': row['ingredients'].split(',')
        }
        for row in db.execute_query(query)
    }


def get_dishes_name(category, origin, show_unavailable):
    query = "SELECT id FROM dish" if show_unavailable else queries["available_dish"]

    if category:
        category_id = get_id(category, "category")
        category_filter = queries['category_filter'].format(category_id=category_id)
        query += f" INTERSECT ({category_filter})"

    if origin:
        origin_ids = [get_id(o, "origin") for o in origin]
        origin_filter = queries['origin_filter'].format(origin_ids=','.join(str(o_id) for o_id in origin_ids),
                                                        len=len(origin_ids))
        query += f" INTERSECT ({origin_filter})"

    return [row["name"] for row in db.execute_query(f"SELECT name FROM dish WHERE id IN ({query})")]


def get_ingredients_details():
    result = db.execute_query(queries["ingredients_details"])
    return {row['name']: row for row in result}


