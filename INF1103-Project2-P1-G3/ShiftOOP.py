from datetime import datetime


class Shift:
    def get_shift(self, now=None):
        now = now or datetime.now()
        hour = now.hour
        if 7 <= hour < 15:      # 07:00 - 14:59
            return "Morning"
        elif 15 <= hour < 23:   # 15:00 - 22:59
            return "Afternoon"
        else:                   # 23:00 - 06:59
            return "Night"