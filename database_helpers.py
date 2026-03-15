import sqlite3
from product import Condition


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
        condition_id = row[0]
        condition_name = row[1]
        condition_description = row[2]

        condition = Condition(
        id=condition_id,
        condition_name=condition_name,
        condition_description=condition_description
        )

        matching_conditions.append(condition)

    return matching_conditions