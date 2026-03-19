import sqlite3
from product import Condition,Product,Symptom,WeeklyPlan


def find_conditions(symptoms):
    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()
    
    symptoms_IN = ", ".join("?" for _ in symptoms)

    cursor.execute(f"""
            SELECT DISTINCT conditions.id,condition_name,condition_description
            FROM conditions
            INNER JOIN symptoms ON conditions.id = symptoms.condition_id
            WHERE LOWER(symptoms.symptom_name) IN ({symptoms_IN})  
        """, symptoms)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    matching_conditions = []  

    for row in rows:
        condition = Condition(
            row[0], #id
            row[1], #condition_name
            row[2]  #condition_description
            )

        matching_conditions.append(condition)

    return matching_conditions


def get_all_conditions():
    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id,condition_name,condition_description FROM conditions")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    conditions = []
    for row in rows:
        condition = Condition(
            row[0], #id
            row[1], #condition_name
            row[2]  #condition_description
        )
        conditions.append(condition)

    return conditions

def get_products(condition_id):
    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, condition_id, product_name, brand, product_type, usage_time, frequency, instructions
        FROM products
        WHERE condition_id = ?
    """, (condition_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = []

    for row in rows:
        product = Product(
            row[0],  # id
            row[1],  # condition_id
            row[2],  # product_name
            row[3],  # brand
            row[4],  # product_type
            row[5],  # usage_time
            row[6],  # frequency
            row[7],  # instructions
        )
        products.append(product)

    return products

def get_weekly_plan():
    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id,day,time_of_day,product_id FROM weekly_plans")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    weekly_plans= []
    for row in rows:
        weekly_plan = WeeklyPlan(
            row[0], #id
            row[1], #day
            row[2], #rime_of_day
            row[3]  #product_id
        )
        weekly_plans.append(weekly_plan)

    return weekly_plans
