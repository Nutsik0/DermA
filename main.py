import sqlite3
import product
from database_helpers import find_conditions




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

def menu():
    while True:   
        print("======Welcome to DermAssist======")
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

check_condition()