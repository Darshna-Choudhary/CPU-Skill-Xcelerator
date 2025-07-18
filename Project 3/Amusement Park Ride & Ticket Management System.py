import json
import os
from collections import deque
from datetime import datetime

v_log = "visitor_log.json"
ride_q = "ride_queue.json"
stk_att = "stk_attraction.json"
tickt_state = "ticket_stats.json"


def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


class ticketSystem():
    def __init__(self):
        self.vip_queue = deque()
        self.regular_queue = deque()
        self.visitor_log = load_data(v_log)
        self.tickt_stat = load_data(tickt_state)
    
    def book(self, name, ticket_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.now().strftime('%Y-%m-%d')
        v_id = "T" + datetime.now().strftime("%H%M%S")

        tickets = {
            "Name" : name,
            "Type" : ticket_type,
            "Time" : timestamp
        }
        
        if ticket_type.lower() == "vip":
            self.vip_queue.append(v_id)
        else:
            self.regular_queue.append(v_id)
        
        if v_id not in self.visitor_log:
            self.visitor_log[v_id] = {
                "ticket" : [],
                "rides_joined" : [],
                "attraction_visited" : []
            }
        self.visitor_log[v_id]["ticket"].append(tickets)

        if date not in self.tickt_stat:
            self.tickt_stat[date] = {}
        
        if ticket_type.lower() not in self.tickt_stat[date]:
            self.tickt_stat[date][ticket_type.lower()] = 0

        self.tickt_stat[date][ticket_type.lower()] += 1

        save_data(v_log, self.visitor_log)
        save_data(tickt_state, self.tickt_stat)

        print(f"Ticket booked for {name} (Visitor ID: {v_id}) in {ticket_type.upper()} queue.")
        return v_id

    def get_next(self):
        if self.vip_queue:
            return self.vip_queue.popleft()
        elif self.regular_queue:
            return self.regular_queue.popleft()
        else:
            print("No visitors in queue.")
            return None

class ride():
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.queue = deque()
    
    def add_to_queue(self, v_id):
        if len(self.queue) >= self.capacity:
            print(f"Ride {self.name} is full.")
            return False
        if v_id in self.queue:
            print(f"{v_id} is already in {self.name}'s queue.")
            return False
        self.queue.append(v_id)
        return True
    
    def proces(self):
        if self.queue:
            return self.queue.popleft()
        return None

class ride_manager():
    def __init__(self):
        self.rides = {}
        ride_data = load_data(ride_q)
        for name in ["Roller Coaster", "Ferris Wheel", "Water Slide"]:
            capacity = 10
            self.rides[name] = ride(name, capacity)
            if name in ride_data:
                self.rides[name].queue = deque(ride_data[name])

    def view_ride(self):
        for name, que in self.rides.items():
            print(f"{name} : {len(que.queue)}/{que.capacity} people in queue")

    def add_v(self, tckt: ticketSystem):
        v_id = tckt.get_next()
        if not v_id:
            print("No visitors waiting in the queue.")
            return
        
        for i, r in enumerate(self.rides.keys(), 1):
            print(f"{i}. {r}")
        choice = int(input("Choose a ride: ")) - 1
        ride_name = list(self.rides.keys())[choice]

        ride = self.rides[ride_name]
        
        if ride.add_to_queue(v_id):
            r_data = load_data(ride_q)
            r_data[ride_name] = list(ride.queue)
            save_data(ride_q, r_data)

            v_data = load_data(v_log)

            if v_id not in v_data:
                v_data[v_id] = {"rides_joined": []}

            v_data[v_id]["rides_joined"].append(ride_name)
            save_data(v_log, v_data)

            print(f"{v_id} added to {ride_name} queue.")
        else:
            print("Already in queue.")

    def process_v(self, r_name):
        if r_name in self.rides and self.rides[r_name]:
            v__id = self.rides[r_name].process()
            save_data(ride_q, self.rides)
            print(f"{v__id} has completed the ride - {r_name}")
            return v__id
        else:
            print("No visitor in ride queue.")
            return None

    def switch_v(self, v_id):
        old_ride = input("Enter your current ride: ").strip()

        if old_ride not in self.rides or v_id not in self.rides[old_ride].queue:
            print("Visitor not in this ride.")
            return
        
        for i, ride in enumerate(self.rides.keys(), 1):
            if ride != old_ride:
                print(f"{i}. {ride}")
        
        new_ride = input("Enter the ride to switch to: ").strip()
        
        if new_ride not in self.rides:
            print("Ride not found! Please choose availbale ride.")
            return
        
        if v_id in self.rides[new_ride].queue:
            print("Already in the ride queue.")
            return
        
        self.rides[old_ride].queue.remove(v_id)
        self.rides[new_ride].add_to_queue(v_id)
        save_data(ride_q, { name: list(ride.queue) for name, ride in self.rides.items() })

        v_log_data = load_data(v_log)
        if v_id not in v_log_data:
            v_log_data[v_id] = {
            "ticket": [],
            "rides_joined": [],
            "attraction_visited": []
        }
        v_log_data[v_id]["rides_joined"].append(new_ride)
        save_data(v_log, v_log_data)
        
        print(f"{v_id} switched from {old_ride} to {new_ride}.")


class stk_attraction():
    def __init__(self):
        self.capacity = 10
        self.attraction = load_data(stk_att) or {
            "Haunted House" : [],
            "Escape Room" : []
        }
        save_data(stk_att, self.attraction)

    def enter(self, v_id):
        for i, name in enumerate(self.attraction.keys(), 1):
            print(f"{i}. {name}")
        choice = int(input("Choose attraction number: ")) - 1
        att = list(self.attraction.keys())[choice]

        if v_id in self.attraction[att]:
            print("You are already inside this attraction.")
            return
        
        if len(self.attraction[att]) >= self.capacity:
            print("Attraction is full! Try again later.")
            return
        
        self.attraction[att].append(v_id)
        save_data(stk_att, self.attraction)

        v_data = load_data(v_log)
        if v_id in v_data:
            v_data[v_id]["attraction_visited"].append({
                "Attraction_name" : att,
                "Time" : datetime.now().strftime("%H:%M:%S")
            })
            save_data(v_log, v_data)
        print(f"{v_id} entered {att}.")

    def exit(self, v_id):
        for name, s in self.attraction.items():
            if s and s[-1] == v_id:
                self.attraction[name].pop()
                save_data(stk_att, self.attraction)
                print(f"{v_id} exited {name}.")
                return
        print("You are either not the last person or not in the stack attraction.")
    
    def curr_status(self):
        for n, s in self.attraction.items():
            inside = ", ".join(s) if s else "Empty"
            print(f"{n} : {len(s)}/{self.capacity} inside. Visitors: {inside}")
        

class admin_panel():
    def __init__(self):
        pass

    def view_queues(self):
        print("\n--- Ride Queues ---\n")
        ride_data = load_data(ride_q)
        if not ride_data:
            print("No ride data found.")
        else:
            for r, q in ride_data.items():
                print(f"\n{r}: {len(q)} visitors in queue: {q}")
        
    def view_stk_att(self):
        print("\n--- Stack-Based Attractions ---\n")
        att_data = load_data(stk_att)
        if not att_data:
            print("No attraction data found.")
        else:
            for att, stk in att_data.items():
                print(f"\n{att}: {len(stk)} visitors inside: {stk}")

    def clear_all_queues(self):
        confirm = input("\nAre you sure you want to clear all queues? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("\nCancelled.")
            return
        save_data(ride_q, {k: [] for k in load_data(ride_q).keys()})
        save_data(stk_att, {k: [] for k in load_data(stk_att).keys()})
        print("\nAll ride queues and attraction stacks cleared.\n")

    def reset_sytem(self):
        confirm = input("\nThis will clear ALL DATA including visitor logs. Confirm? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("\nCancelled.")
            return
        
        ride_data = load_data(ride_q)
        att_data = load_data(stk_att)
        vdata = load_data(v_log)

        os.makedirs("Backup", exist_ok=True)

        timestamp = datetime.now().strftime("Y-%m-%d_%H-%M-%S")
        backup_file = f"Backup/backup_{timestamp}.json"

        with open(backup_file, "w") as f:
            json.dump({
                "ride_q": ride_data,
                "stk_att": att_data,
                "v_log": vdata
            }, f, indent=4)
        
        print(f"\nBackup created at {backup_file}")
        
        save_data(ride_q, {})
        save_data(stk_att, {})
        save_data(v_log, {})
        print("\nSystem has been fully reset.\n")


def main():
    ts = ticketSystem()
    rm = ride_manager()
    stk = stk_attraction()
    ad = admin_panel()
    print("\n========= Welcome to FunZone Amusement Park =========\n")

    while True:
        v_or_a = int(input("(1)Visitor, (2)Admin, (3)Exit\n"))
        match v_or_a:
            case 1:
                visitor_menu(ts, rm, stk)
            case 2:
                admin_menu(ts, rm, stk, ad)
            case 3:
                print("Exiting")
                break
            case _:
                print("Invalid choice")


def visitor_menu(ts, rm, stk):
    while True:
        v_choice = input("Please choose an option ->\n" \
            "1.) Buy ticket\n    -> Choose VIP or Regular\n\n" \
            "2.) View available rides\n\n" \
            "3.) Join Ride Queue\n    -> Select a ride to enter the queue\n\n" \
            "4.) Switch Ride\n" \
            "5.) Enter Stack Attraction\n    -> Haunted House / Escape Room\n\n" \
            "6.) View my visit history\n    -> Ticket type, Rides joined, Attractions visited\n\n" \
            "7.) Exit park\n    -> Thank you! Your visit has been logged\n")
        match v_choice:
            case '1' :
                print("Choose ticket type:")
                tckt_type = input("VIP or Regular: ").strip()
                name = input("Enter your name: ").strip()
                id = ts.book(name, tckt_type)
            case '2':
                rm.view_ride()
            case '3':
                rm.add_v(ts)
            case '4':
                v_id = input("Enter you Visitor ID: ")
                rm.switch_v(v_id)
            case '5':
                v_id = input("Enter your Visitor ID: ")
                while True:
                    print("\n--- Attraction Menu ---")
                    print("1. Enter Attraction")
                    print("2. Exit Attraction")
                    print("3. Back to Main Menu")
                    ch = input("Enter your choice: ").strip()
                    if ch == '1':
                        stk.enter(v_id)
                    elif ch == '2':
                        stk.exit(v_id)
                    elif ch == '3':
                        break
                    else:
                        print("Invalid option.")
            case '6':
                vid = input("Enter your Visitor ID: ")
                data = load_data(v_log)
                if vid in data:
                    print("\n--- Visit History ---")
                    print("Tickets:")
                    for t in data[vid]["ticket"]:
                        print(f"{t["Type"].upper()} at {t["Time"]}")
                    print("Rides Joined:",", ".join(data[vid]["rides_joined"]) or "None")
                    print("Attractions Visited:")
                    for att in data[vid]["attraction_visited"]:
                        print(f"{att["Attraction_name"]} at {att["Time"]}")
                else:
                    print("Visitor not found.")
            case '7':
                print("Exiting")  
                break
            case _:
                print("Invalid choice")


def admin_menu(ts, rm, stk, ad):
    print("============== ADMIN PANEL ==============\n")
    while True:
        a_choice = input("1.) View Visitor History\n\n" \
            "2.) View Ride Queue Status\n\n" \
            "3.) View Stack Attraction Status\n\n" \
            "4.) View Ticket Sales Summary\n\n"\
            "5.) Clear All Queues\n\n" \
            "6.) Reset System for New Day\n\n" \
            "7.) Exit Admin Panel\n")
        match a_choice:
            case '1':
                v_data = load_data(v_log)
                print_visitor_log(v_data)
            case '2':
                ad.view_queues()
            case '3':
                ad.view_stk_att()
            case '4':
                tickt = load_data(tickt_state)
                print_ticket_summary(tickt)
            case '5':
                ad.clear_all_queues()
            case '6':
                ad.reset_sytem()
            case '7':
                print("Exiting")
                break
            case _:
                print("Invalid choice")

def print_visitor_log(visitor_log: dict):
    print("\n======= VISITOR LOG =======\n")

    for v_id, data in visitor_log.items():
        print(f"Visitor ID: {v_id}")

        ticket_key = "ticket" if "ticket" in data else "tickets"
        tickets = data.get(ticket_key, [])
        for t in tickets:
            print(f"  Name        : {t.get('Name')}")
            print(f"  Ticket Type : {t.get('Type').capitalize()}")
            print(f"  Entry Time  : {t.get('Time')}")

        rides = data.get("rides_joined", [])
        if rides:
            print(f"  Rides Joined: {', '.join(rides)}")
        else:
            print("  Rides Joined: None")

        attractions = data.get("attraction_visited", [])
        if attractions:
            print("  Attractions Visited:")
            for a in attractions:
                print(f"    - {a['Attraction_name']} at {a['Time']}")
        else:
            print("  Attractions Visited: None")

        print("-" * 35)

    print("\n======= END OF LOG =======\n")

def print_ticket_summary(summary: dict):
    print("\n======= TICKET SUMMARY =======\n")
    print(f"{'Date':<15} {'Regular Tickets':<18} {'VIP Tickets':<12} {'Total'}")
    print("-" * 55)

    for date in sorted(summary.keys()):
        regular = summary[date].get('regular', 0)
        vip = summary[date].get('vip', 0)
        total = regular + vip
        print(f"{date:<15} {regular:<18} {vip:<12} {total}")

    print("\n======= END OF SUMMARY =======\n")

if __name__ == "__main__":
    main()
