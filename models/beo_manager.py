from utils.text_formatter import TextFormatter

class BEOManager:
    def __init__(self):
        self.dates = []  # List of Date objects

    def add_date(self, date):
        self.dates.append(date)

    def remove_date(self, date):
        if date in self.dates:
            self.dates.remove(date)

    def get_date_by_str(self, date_str):
        for date in self.dates:
            if date.date_str == date_str:
                return date
        return None

    def get_all_dates(self):
        return self.dates

    def get_formatted_text(self):
        return TextFormatter.format_beo(self.dates)
