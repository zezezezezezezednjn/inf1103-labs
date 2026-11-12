import json
import sqlite3
from datetime import date, datetime

# ==========================================
# Connect to Database
# ==========================================

def connect_db():
    conn = sqlite3.connect("database.db")

    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON")

    return conn

# ==========================================
# Check if Table Exists
# ==========================================
def table_exists(table_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?
    """, (table_name,))

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==========================================
# Create Tables
# ==========================================

def create_handover_table():
    conn = connect_db()
    cursor = conn.cursor()

    already_exists = table_exists("handover")

    # Create handover table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS handover (
            handover_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            shift TEXT NOT NULL,
            remarks TEXT
        )
    """)

    conn.commit()
    conn.close()

    if already_exists:
        print("Handover table found.")
    else:
        print("Handover table created.")

def create_task_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    already_exists = table_exists("task")

    # Create task table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            handover_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            due_date TEXT,
            shifts_pending INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY (handover_id)
                REFERENCES handover(handover_id)
        )
    """)

    conn.commit()
    conn.close()

    if already_exists:
        print("Task table found.")
    else:
        print("Task table created.")

# ==========================================
# Add Handover
# ==========================================

def add_handover(date, shift, remarks=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO handover (
            date,
            shift,
            remarks
        )
        VALUES (?, ?, ?)
    """, (
        date,
        shift,
        remarks
    ))

    cursor.execute("UPDATE Task SET shifts_pending = shifts_pending + 1 WHERE status = 'pending'")

    # Get the ID that SQLite automatically created
    handover_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return handover_id

# ==========================================
# Get Handover
# ==========================================
def get_handovers():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM handover
    """)

    handovers = cursor.fetchall()

    conn.close()

    return handovers

# ==========================================
# Add Task
# ==========================================

def add_task(
        handover_id,
        description,
        status="pending",
        due_date=None,
        shifts_pending=0
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO task (
            handover_id,
            description,
            status,
            due_date,
            shifts_pending
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        handover_id,
        description,
        status,
        due_date,
        shifts_pending
    ))

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return task_id

# ==========================================
# Update Task Status
# ==========================================
def update_task_status(task_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task
        SET status = ?
        WHERE task_id = ?
    """, (
        new_status,
        task_id
    ))

    conn.commit()
    conn.close()

# ==========================================
# Get Tasks
# ==========================================
def get_tasks(handover_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM task
        WHERE handover_id = ?
    """, (handover_id,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks

# ==========================================
# Get Pending Tasks
# ==========================================
def get_pending_tasks():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, description, status, shifts_pending
        FROM task
        WHERE status = 'pending'
    """)
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

# ==========================================
# Save Records from AI
# ==========================================
def _save_one(record):
    pending = get_pending_tasks()      # list of dicts
    pending_ids = {t["task_id"] for t in pending}
    by_description = {t["description"].strip().lower(): t["task_id"] for t in pending}

    def find_existing(task):
        task_id = task.get("task_id")
        if task_id in pending_ids:
            return task_id
        return by_description.get(task["description"].strip().lower())

    matched = [(task, find_existing(task)) for task in record["tasks"]]

    # 1. Mark existing tasks completed
    for task, existing_id in matched:
        if existing_id is not None and task["status"] == "completed":
            update_task_status(existing_id, "completed")

    # 2. Add the handover
    handover_id = add_handover(
        record.get("date") or date.today().isoformat(),
        record.get("shift") or "Unknown",
        record.get("remarks"),
    )

    # 3. Add only genuinely new tasks
    for task, existing_id in matched:
        if existing_id is not None:
            continue
        add_task(
            handover_id=handover_id,
            description=task["description"],
            status=task["status"],
            due_date=task.get("due_date"),
            shifts_pending=task.get("shifts_pending") or 0,
        )


def save_record(ai_result):
    """ai_result can be a JSON string, or already-parsed list/dict."""
    try:
        data = json.loads(ai_result) if isinstance(ai_result, str) else ai_result
        records = data if isinstance(data, list) else [data]

        for record in records:
            _save_one(record)
        return True

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Could not save record: {type(e).__name__}: {e!r}")
        return False
# ==========================================
# Using of function
# ==========================================

## Create tables if they do not already exist
# create_handover_table()
# create_task_table()
    


# #   Create a new handover
# handover_id = add_handover(
#     date="2026-09-30",
#     shift="Morning",
#     remarks="Machine 4 requires further monitoring"
# )


# # Add tasks to that handover
# add_task(
#     handover_id=handover_id,
#     description="Complete safety inspection",
#     status="completed",
# )

# add_task(
#     handover_id=handover_id,
#     description="Inspect Machine 4",
#     status="pending",
#     due_date="2026-10-01",
#     shifts_pending=1
# )

# #   Create a new handover
# handover_id = add_handover(
#     date="2026-09-30",
#     shift="Afternoon",
#     remarks="Machine 5 requires further monitoring"
# )


# # Add tasks to that handover
# add_task(
#     handover_id=handover_id,
#     description="Complete safety inspection",
#     status="completed",
# )

# add_task(
#     handover_id=handover_id,
#     description="Inspect Machine 5",
#     status="pending",
#     due_date="2026-10-02",
#     shifts_pending=0
# )

## Retrieve and display handovers and their tasks
# handovers = get_handovers()

# for handover in handovers:
#     #To print handover ID
#     # print(handover[0])
#     #Print tasks using handover ID
#     tasks = get_tasks(handover[0]) 

#     for task in tasks:
#         print("Task ID:", task[0])
#         print("Handover ID:", task[1])
#         print("Description:", task[2])
#         print("Status:", task[3])
#         print("Due Date:", task[4])
#         print("Shifts Pending:", task[5])
#         print("-----------------------------")

##Update Task Status using Task ID and new status
# update_task_status(1, "completed")