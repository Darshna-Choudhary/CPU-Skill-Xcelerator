def read_file(file):
    data = {}
    with open(file, 'r') as f:
        for line in f:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip().title()] = value.strip()
        return data

def validate(data):
    errors = []
    phone = data["Phone_No"]
    if '@' not in data["Email"] or '.' not in data["Email"]:
        errors.append("Invalid email")
    if not phone.isdigit() or len(phone) != 10:
        errors.append("Phone number should consist of only 10 digits")
    if not data["Skills"]:
        errors.append("Skills section missing")
    if not data["Experience"]:
        errors.append("Experience section missing")
    return errors

def formatted_file(data):
    name = data["Name"].title()
    skill = ", ".join([s.strip().title() for s in data["Skills"].split(',')])
    txt = "\n----------Formatted Resume----------\n\n"
    txt += f"Name : {name}\n"
    txt += f"Phone No. : {data["Phone_No"]}\n"
    txt += f"Email : {data["Email"]}\n"
    txt += f"Skills : {skill}\n"
    txt += f"Experience : {data["Experience"]}\n"
    return txt

def main():
    inp_file = input("Enter resume .txt file\n")
    raw_file = read_file(inp_file)
    error = validate(raw_file)
    print(formatted_file(raw_file))

    if error:
        print("----------Issues In Resume----------")
        for e in error:
            print("-> ", e)
    else:
        print("----------Resume Is Correct----------")

if __name__ == "__main__":
    main()
