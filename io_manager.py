from datetime import datetime

SHIFTS = ["Morning", "Afternoon", "Night"]
STATUS = ["Completed", "In Progress"]
PRIORITY = ["High", "Medium", "Low"]
tasks = []

def date_format(value):
    if len(value) != 10:
        return False
    elif datetime.strptime(value, "%Y-%m-%d"):
        return True
    else:
        return False

def get_date():
    while True:
        date = input("Date (YYYY-MM-DD): ")
        if date_format(date):
            return date
        else:
            print("Invalid Date")

def get_shift():
    while True:
        shift = input("Shift (Morning, Afternoon, Night): ")
        if shift in SHIFTS:
            return shift
        else:
            print("Invalid Shift")

def get_status():
    while True:
        status = input("Status (Completed, In Progress): ")
        if status in STATUS:
            return status
        else:
            print("Invalid Status")

def get_due_due():
    while True:
        due_date = input("Due Date (YYYY_MM_DD):")
        if date_format(due_date):
            return due_date
        else:
            print("Invalid Date")

def get_remarks():
    return input("Remarks: ")

def get_priority():
    while True:
        priority = input("Priority of task (High, Medium, Low): ")
        if priority in PRIORITY:
            return priority
        else:
            print("Invalid Input")

date = get_date()
shift = get_shift()

while True:
    task = input("Task ('quit' to exit): ")
    if task == "quit":
        break

    tasks.append({
        "task": task,
        "status": get_status(),
        "due_date": get_due_due(),
        "remarks": get_remarks(),
        "priority": get_priority()
    })

print(tasks)




