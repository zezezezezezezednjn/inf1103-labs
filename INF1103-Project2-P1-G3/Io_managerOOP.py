from datetime import date

import data_manager as db
from InputHandlerOOP import InputHandler
from ShiftOOP import Shift
from DisplayOOP import Display


class IOManager:
    def __init__(self):
        self.input_handler = InputHandler()
        self.shift = Shift()
        self.display = Display()

    def get_input(self):
        self.display.print_records()      # reads the database and shows ongoing tasks
        today = date.today().isoformat()

        completed = None
        ongoing = None

        while True:
            if completed is None:
                completed = self.input_handler.get_completed()
                if completed == "" and not self.input_handler.confirm_empty("completed"):
                    completed = None   # n -> ask completed again
                    continue

            if ongoing is None:
                ongoing = self.input_handler.get_ongoing()
                if ongoing == "" and not self.input_handler.confirm_empty("ongoing"):
                    ongoing = None   # n -> ask ongoing again
                    continue

            remarks = self.input_handler.get_remarks()
            break

        shift = self.shift.get_shift()

        return today, shift, completed, ongoing, remarks

    def save_input(self, today, shift, completed, ongoing, remarks):
        handover_id = db.add_handover(today, shift, remarks)

        if completed != "":
            db.add_task(handover_id, completed, "completed")
        if ongoing != "":
            db.add_task(handover_id, ongoing, "pending")

    def show_output(self):
        self.display.display_output()