use emenu;

DROP TABLE IF EXISTS Dish_Origin;
DROP TABLE IF EXISTS Dish_Ingredient;
DROP TABLE IF EXISTS MenuSchedule;

DROP TABLE IF EXISTS Dish;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Origin;
DROP TABLE IF EXISTS ServingHours;
DROP TABLE IF EXISTS Unit;

CREATE TABLE Category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Origin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE ServingHours (
    id INT PRIMARY KEY,
    start TIME NOT NULL,
    end TIME NOT NULL
);

CREATE TABLE Unit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Ingredient (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    quantity DECIMAL(10, 2) NOT NULL,
    import_date DATE NOT NULL,
    expired_date DATE NOT NULL,
    unit_id INT,
    FOREIGN KEY (unit_id) REFERENCES Unit(id) ON DELETE SET NULL
);

CREATE TABLE Dish (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) CHECK (price > 0) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE SET NULL
);

CREATE TABLE Dish_Origin(
    dish_id INT,
    origin_id INT,
    FOREIGN KEY (dish_id) REFERENCES Dish(id) ON DELETE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES Origin(id) ON DELETE CASCADE,
    UNIQUE KEY (dish_id, origin_id)
);

CREATE TABLE Dish_Ingredient (
    dish_id INT,
    ingredient_id INT,
    FOREIGN KEY (dish_id) REFERENCES Dish(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id) ON DELETE CASCADE,
    UNIQUE KEY (dish_id, ingredient_id)
);

CREATE TABLE MenuSchedule (
    dish_id INT,
    time_id INT,
    FOREIGN KEY (dish_id) REFERENCES Dish(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES ServingHours(id) ON DELETE CASCADE,
    UNIQUE KEY (dish_id, time_id)
);


