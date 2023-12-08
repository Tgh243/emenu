queries = {
    "price": f"SELECT price FROM dish WHERE dish.id=%s",

    "category": """
    SELECT category.name
    FROM category
    JOIN dish ON category_id=category.id
    WHERE dish.id=%s
    """,

    "origin": """
    SELECT origin.name
    FROM origin
    JOIN dish_origin ON origin_id=origin.id
    WHERE dish_origin.dish_id=%s
    """,

    "ingredient_details": """
    SELECT quantity, unit.name as unit, import_date, expired_date
    FROM ingredient
    JOIN unit ON unit_id=unit.id
    WHERE ingredient.name=%s
    """,

    "dish_ingredient": """
    SELECT ingredient.name
    FROM ingredient
    JOIN dish_ingredient ON ingredient_id=ingredient.id
    JOIN dish ON dish_id=dish.id
    WHERE dish.id=%s
    """,

    "available_dish": """
    SELECT DISTINCT ms.dish_id
    FROM menuschedule ms
    INNER JOIN servinghours sh ON ms.time_id = sh.id
    WHERE current_time() BETWEEN start AND end
    """,

    "serving_hours": """
    SELECT start, end
    FROM servinghours 
    inner join  
    WHERE dish.id=%s
    """
}
