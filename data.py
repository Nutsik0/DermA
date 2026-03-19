import sqlite3

conn = sqlite3.connect("dermassist.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_name TEXT NOT NULL,
    condition_description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    condition_id INTEGER,
    product_name TEXT,
    brand TEXT,
    product_type TEXT,
    usage_time TEXT,
    frequency TEXT,
    instructions TEXT,
    FOREIGN KEY(condition_id) REFERENCES conditions(id)
);

CREATE TABLE IF NOT EXISTS  symptoms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom_name TEXT,
    condition_id INTEGER,
    FOREIGN KEY(condition_id) REFERENCES conditions(id)                 
);                 
""")

conditions_data = [
('Acne','Inflammatory skin condition affecting hair follicles'),

('Rosacea','Chronic skin condition causing redness and flushing'),

('Seborrheic Dermatitis','Inflammatory condition affecting oily areas')
]

cursor.executemany(
"INSERT INTO conditions (condition_name,condition_description) VALUES (?,?)",
conditions_data
)

products_data = [
(1,'Effaclar Purifying Foaming Gel','La Roche-Posay','Cleanser','morning','daily','Wash face gently for 30 seconds'),
(1,'CeraVe Foaming Facial Cleanser','CeraVe','Cleanser','night','daily','Clean skin before applying treatments'),
(1,'Effaclar Duo','La Roche-Posay','Acne Treatment','night','daily','Apply thin layer to acne areas'),
(1,'CeraVe AM Facial Moisturizing Lotion','CeraVe','Moisturizer','morning','daily','Apply after cleansing'),

(2,'Toleriane Hydrating Gentle Cleanser','La Roche-Posay','Cleanser','morning','daily','Use gentle cleanser to avoid irritation'),
(2,'Azelaic Acid Suspension 10%','The Ordinary','Treatment','night','daily','Apply small amount to affected areas'),
(2,'Rosaliac AR Intense Serum','La Roche-Posay','Serum','morning','daily','Apply to reduce redness'),
(2,'Cetaphil Redness Relieving Moisturizer','Cetaphil','Moisturizer','morning','daily','Hydrate sensitive skin'),

(3,'Nizoral Ketoconazole Shampoo','Nizoral','Medicated Shampoo','morning','3x weekly','Apply to scalp and leave for 5 minutes'),
(3,'Head & Shoulders Classic Clean','Head & Shoulders','Anti-Dandruff Shampoo','morning','daily','Use regularly to control dandruff'),
(3,'Bioderma Sensibio DS+ Cream','Bioderma','Treatment Cream','night','daily','Apply thin layer to affected areas'),
(3,'CeraVe Moisturizing Cream','CeraVe','Moisturizer','night','daily','Apply to dry or irritated skin')
]

cursor.executemany("""
INSERT INTO products
(condition_id, product_name, brand, product_type, usage_time, frequency, instructions)
VALUES (?,?,?,?,?,?,?)
""", products_data)

symptoms_data = [
('Pimples',1), 
('blackheads',1),
('whiteheads',1), 
('oily skin',1),
('Redness',2),
('flushing',2),
('visible blood vessels',2),
('Dandruff',3),
('redness',3),
('greasy scales',3)
]

cursor.executemany("""INSERT INTO symptoms (symptom_name,condition_id) VALUES(?,?)""", symptoms_data)

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS weekly_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    time_of_day TEXT,
    product_id INTEGER
);
""")


conn.commit()
conn.close()



