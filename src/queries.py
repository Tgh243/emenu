queries = {

    "origins":
    """
    SELECT dish.id, GROUP_CONCAT(origin.name) AS origins
    FROM dish
    INNER JOIN dish_origin ON dish_id=dish.id
    INNER JOIN origin ON origin_id=origin.id
    GROUP BY dish.id
    """,

    "ingredients":
    """
    SELECT dish.id, GROUP_CONCAT(ingredient.name) AS ingredients
    FROM dish
    INNER JOIN dish_ingredient ON dish_id=dish.id
    INNER JOIN ingredient ON ingredient_id=ingredient.id
    GROUP BY dish.id
    """,

    "dishes_details":
    """
    SELECT dish.name, price, category.name AS category, o.origins, i.ingredients
    FROM dish
    INNER JOIN category ON category_id=category.id
    INNER JOIN ({origins}) AS o ON o.id=dish.id
    INNER JOIN ({ingredients}) AS i ON i.id=dish.id
    """,

    "ingredients_details":
    """
    SELECT ingredient.name, quantity, unit.name AS unit, import_date, expired_date
    FROM ingredient
    JOIN unit ON unit_id=unit.id
    """,

    "available_dish":
    """
    SELECT DISTINCT ms.dish_id
    FROM menuschedule AS ms
    INNER JOIN servinghours AS sh ON ms.time_id = sh.id
    WHERE current_time() BETWEEN start AND end
    """,

    "category_filter":
    """
    SELECT dish.id 
    FROM dish 
    WHERE category_id={category_id}
    """,

    "origin_filter":
    """
    SELECT dish_id
    FROM dish_origin
    WHERE origin_id IN ({origin_ids})
    GROUP BY dish_id
    HAVING COUNT(origin_id)={len}
    """

}
