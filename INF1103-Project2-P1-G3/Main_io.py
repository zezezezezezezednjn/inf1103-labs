import os

# always work from this file's folder, so the right database.db is used
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import data_manager as db
from Io_managerOOP import IOManager

print("Using database:", os.path.abspath("database.db"))   # remove once it works

db.create_handover_table()
db.create_task_table()

io = IOManager()
today, shift, completed, ongoing, remarks = io.get_input()
io.save_input(today, shift, completed, ongoing, remarks)
io.show_output()