import json
import os

file = "patient.json"

def load_patient():
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_patient(patients):
    with open(file, "w") as f:
        json.dump(patients, f, indent=2)

def is_critical(vitals):
    alert = []
    temp = float(vitals["Temperature"])
    bp = vitals["BP"]
    bp_high, bp_low = map(int, bp.split('/'))
    hr = int(vitals["Heart_Rate"])
    if temp > 100 or bp_high > 140 or bp_low > 90 or hr > 100:
        alert.append("Alert: Patient vitals are in critical range! Immediate attention required.")
    return alert

def new_record():
    patients = load_patient()
    id = input("Enter patient ID - ")
    name = input("Enter patient's name - ")
    age = int(input("Enter patient's age - "))
    gender = input("Enter patient's gender - ")
    temp = float(input("Enter patient's temperature - "))
    bp = input("Enter patient's blood pressure - ")
    hr = int(input("Enter patient's heart rate - "))
    data = {
        "Name" : name,
        "Age" : age,
        "Gender" : gender,
        "Vitals" : {
            "Temperature" : temp,
            "BP" : bp,
            "Heart_Rate" : hr
        }
    }
    patients[id] = data
    save_patient(patients)
    print("Patient", name, "added successfully!")
    a = is_critical(data["Vitals"])
    if a:
        print(a,"\n")


def view_patient():
    p = load_patient()
    if not p:
        print("No record found!")
        return
    print("Patient Records:")
    print("-"*50)
    for id, detail in p.items():
        name = detail["Name"]
        age = detail["Age"]
        gen = detail["Gender"]
        vit = detail["Vitals"]
        temp = vit["Temperature"]
        bp = vit["BP"]
        hr = vit["Heart_Rate"]
        print(f"ID: {id} | Name: {name} | Age: {age} | Temp: {temp}°F | BP: {bp} | HR: {hr} bpm")
        print("-"*50)
        a = is_critical(vit)
        if a:
            print(a,"\n")


def search_patient(p_id):
    p = load_patient()
    found = False
    for id, detail in p.items():
        if p_id.strip() == id:
            print("Record Found:")
            print(f"Name : {detail['Name']}")
            print(f"Age : {detail['Age']}")
            print(f"Temperature : {detail['Vitals']['Temperature']}")
            print(f"BP : {detail['Vitals']['BP']}")
            print(f"Heart_Rate : {detail['Vitals']['Heart_Rate']}")
            a = is_critical(detail['Vitals'])
            if a:
                print(a,"\n")
            found = True
            break
    if not found:
        print("No record found")


def update_vitals():
    p = load_patient()
    id = input("Enter ID: ")
    if id in p:
        newtemp = float(input("New Temperature : "))
        newbp = input("New BP: ")
        newhr = int(input("New HR: "))
        p[id]["Vitals"]["Temperature"] = newtemp
        p[id]["Vitals"]["BP"] = newbp
        p[id]["Vitals"]["Heart_Rate"] = newhr
        save_patient(p)
        print("Vitals updated for patient",p[id]["Name"])
        a =  is_critical(p[id]["Vitals"])
        if a:
            print(a,"\n")
    else:
        print("No record found!")

def delete_record():
    p = load_patient()
    id = input("Enter patient ID to be deleted - ").strip()
    if id in p:
        del p[id]
        save_patient(p)
        print("Patient record for ID",id,"deleted.")
    else:
        print("Id not found.")

def main():
    
    while True:
        inp = input("Select an option given below:-\n" \
        "1.) Add a new patients\n" \
        "2.) View all patients' records\n" \
        "3.) Search patient\n" \
        "4.) Update patient's record\n" \
        "5.) Delete a patient's record\n" \
        "6.) Exit\n")
        match inp:
            case "1":
                n = int(input("How many patients' records do you want to enter\n"))
                for i in range(n):
                    new_record()
            case "2":
                view_patient()
            case "3":
                patient_id = input("Enter patient id to be searched\n")
                search_patient(patient_id)
            case "4":
                update_vitals()
            case "5":
                delete_record()
            case "6":
                print("Existing")
                break
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    main()
