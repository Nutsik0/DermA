import sqlite3
from product import Product, Condition, Symptom
from database_helpers import find_conditions,get_all_conditions,get_products,get_weekly_plan
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler() 

def check_condition():
    symptom_input = input("Enter symptoms seperated by commas :")
    split_symptoms = symptom_input.split(",")
    symptoms= []
    for i in split_symptoms:
        clean_symptoms = i.strip()
        if clean_symptoms != "":
            symptoms.append(clean_symptoms.lower())

    if len(symptoms) == 0:
        print(" No symptoms entered.")
        return
    
    print("You entered these symptoms:", symptoms)
    print(f"Searching conditions for: {",".join(symptoms)}")
    
    matching_conditions = find_conditions(symptoms)
    if matching_conditions :
        for condition in matching_conditions:
            print(condition.condition_name)
    else:
        print("No matching conditions found for these symptoms.")
        

def view_all_conditions():
    conditions = get_all_conditions()
    print("All skin conditions in our system are : ")
    for condition in conditions:
        print(f"{condition.condition_name} - {condition.condition_description}")
    

def show_products():
    conditions = get_all_conditions()
    print("--- Skin Conditions ---")
    for num,con in enumerate(conditions, start=1):
        print(f"{num}. {con.condition_name}")

    choice_str = input("Enter the number of the condition to see products: ").strip()  

    if not choice_str.isdigit():
        print("Please enter a valid number.")
        return

    choice_num = int(choice_str)

    if choice_num < 1 or choice_num > len(conditions):
        print("Number out of range. Please try again.")
        return
    
    selected_condition = conditions[int(choice_str)-1]

    products = get_products(selected_condition.id)
    if not products: 
        print("No products found for this condition.") 
        return
    
    print(f"Recommended products for {selected_condition.condition_name}:") 

    for p in products: 
        print("-------------------------")
        print(p)
        

def generate_plan():
    conditions = get_all_conditions()
    print("--- Skin Conditions ---")
    for num,con in enumerate(conditions, start=1):
        print(f"{num}. {con.condition_name}")

    choice_str = input("Enter the number of the condition : ").strip()  

    if not choice_str.isdigit():
        print("Please enter a valid number.")
        return

    choice_num = int(choice_str)

    if choice_num < 1 or choice_num > len(conditions):
        print("Number out of range. Please try again.")
        return
    
    selected_condition = conditions[int(choice_str)-1]

    products = get_products(selected_condition.id)

    if not products:
        print("No products found.")
        return

    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM weekly_plans")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week_3x_days = ["Monday", "Wednesday", "Friday"]

    products.sort(key=lambda p: p.usage_time)

    daily_products = [p for p in products if p.frequency == "daily"]
    weekly_products = [p for p in products if p.frequency == "3x weekly"]

    for day in days:
        for product in daily_products:
            cursor.execute("""
                INSERT INTO weekly_plans (day, time_of_day, product_id)
                VALUES (?, ?, ?)
            """, (day, product.usage_time, product.id))

    for day in week_3x_days:
        for product in weekly_products:
            cursor.execute("""
                INSERT INTO weekly_plans (day, time_of_day, product_id)
                VALUES (?, ?, ?)
            """, (day, product.usage_time, product.id))


    conn.commit()
    conn.close()

    print("Weekly plan created successfully!")


def view_plan():
    conn = sqlite3.connect("dermassist.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT day, time_of_day, product_id
        FROM weekly_plans
    """)

    rows = cursor.fetchall()

    current_day = None
    current_time = None

    for row in rows:
        day, time_of_day, product_id = row
        if day != current_day or time_of_day != current_time:
            print("---------------")
            print(f"{day} ({time_of_day})")
            current_day = day
            current_time = time_of_day

        cursor.execute("""
            SELECT product_name, brand, product_type, usage_time, frequency, instructions
            FROM products
            WHERE id = ?
        """, (product_id,))

        product = cursor.fetchone()

        print(f"- {product[0]} by {product[1]}")
        print(f"  {product[2]}")
        print(f"  Usage: {product[3]}, Frequency: {product[4]}")
        print(f"  Instructions: {product[5]}")

    conn.close()

def reminder():
    weekly_plans= get_weekly_plan()
    products = get_products()
    current_day = datetime.now().strftime("%A")
    current_hour = datetime.now().hour
    
    current_time_of_day = "morning" if current_hour == 12 else "night"

    for weekly_plan in weekly_plans:
        if weekly_plan.day == current_day and weekly_plan.time_of_day == current_time_of_day:
            product = [prod for prod in products if prod.id == weekly_plan.product_id]
            
            print(f"use {product}")
            
    
def start_worker() :
    scheduler.add_job(reminder, 'cron', hour=12, minute=0)
    scheduler.add_job(reminder, 'cron', hour=21, minute=0)

    scheduler.start()

def stop_worker():
    if scheduler.running:
        scheduler.shutdown()
        print("Reminder service stopped.")
    else:
        print("Reminder service is not running.")


def menu():
    while True:   
        print("----------------------")
        print("======DermAssist======")
        print("1. Check skin condition by symptoms")
        print("2. View all skin conditions")
        print("3. View recommended products for a condition")
        print("4. Generate weekly skincare plan")
        print("5. View my weekly plan")
        print("6. Start reminder service")
        print("7. Stop reminder service")
        print("8. Exit")

        try:
            choice = int(input("Choose an option (1-8): ").strip())

            if choice < 1 or choice > 8:
                print("Invalid option. Please enter a number between 1 and 8.")
                continue

            if choice == 1:
                check_condition()
            elif choice == 2:
                view_all_conditions()
            elif choice == 3:
                show_products()
            elif choice == 4:
                generate_plan()
            elif choice == 5:
                view_plan()
            elif choice == 6:
                start_worker()
            elif choice == 7:
                stop_worker()
            elif choice == 8:
                print("Goodbye!")
                break

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")

menu()