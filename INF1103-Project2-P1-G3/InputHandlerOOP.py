import sys


class InputHandler:
    def check_quit(self, value):
        if value.lower() == "quit":
            print("Exiting program.")
            sys.exit()

    def get_completed(self):
        value = input("\nCompleted task: ")
        self.check_quit(value)
        return value

    def get_ongoing(self):
        value = input("Ongoing task: ")
        self.check_quit(value)
        return value

    def get_remarks(self):
        value = input("Remarks: ")
        self.check_quit(value)
        return value

    def confirm_empty(self, name):
        answer = input(f"No {name} task entered. Do you want to continue? (y/n): ")
        return answer.lower() == "y"