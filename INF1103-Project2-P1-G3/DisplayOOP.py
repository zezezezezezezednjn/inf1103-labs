import data_manager as db


class Display:
    def show_tasks(self, title, tasks):
        print(title)
        if len(tasks) == 0:
            print("None")
        for task in tasks:
            print("  - " + task[2])
        print()

    def print_records(self):
        handovers = db.get_handovers()
        if handovers == []:
            print("\nNo records found.\n")
            return
        print("\nCurrent ongoing tasks:")
        for handover in handovers:
            for task in db.get_tasks(handover[0]):
                if task[3] == "pending":
                    print(f"- {task[2]}")
        print("\nRemarks from last shift:")
        print(f"- {handovers[-1][3]}")

    def display_output(self):
        handovers = db.get_handovers()
        if len(handovers) == 0:
            print("No records found.\n")
            return

        latest = handovers[-1]

        ongoing = []
        for handover in handovers:
            for task in db.get_tasks(handover[0]):
                if task[3] == "pending":
                    ongoing.append(task)

        completed = []
        for task in db.get_tasks(latest[0]):
            if task[3] == "completed":
                completed.append(task)

        self.show_tasks("\nOngoing Task:", ongoing)
        self.show_tasks("Completed Task:", completed)

        print("Remarks:")
        if latest[3] is None or len(latest[3]) == 0:
            print("  None")
        else:
            print("  - " + latest[3])