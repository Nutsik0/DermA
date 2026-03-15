class Product():
    def __init__(self,id,condition_id,product_name,brand,product_type,usage_time,frequency,instructions):
        self.id = id
        self.condition_id = condition_id
        self.product_name = product_name
        self.brand = brand
        self.product_type = product_type
        self.usage_time = usage_time
        self.frequency = frequency
        self.instructions = instructions

    def __str__(self):
        return (f"{self.product_name} by {self.brand} ({self.product_type})\n"
                f"Usage: {self.usage_time}, Frequency: {self.frequency}\n"
                f"Instructions: {self.instructions}")

class Symptom():
    def __init__(self,id,symptom_name,condition_id):
        self.id = id
        self.symptom_name = symptom_name
        self.condition_id = condition_id
    
    def __str__(self):
        return f"Symptom: {self.symptom_name}"

class Condition():
    def __init__(self,id,condition_name,condition_description):
        self.id = id
        self.condition_name = condition_name
        self.condition_description = condition_description

    
    def __str__(self):
        return f"{self.condition_name} - {self.condition_description}"