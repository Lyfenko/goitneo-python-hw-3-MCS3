from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        while not self.is_valid_phone(value):
            value = input(
                "Phone number must be a 10-digit number. Please enter a 10-digit phone number: "
            )
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday format. Please use DD.MM.YYYY.")
        super().__init__(value)

    @staticmethod
    def is_valid_birthday(value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_str}, birthday: {str(self.birthday)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        name = name.lower()
        for key in self.data:
            if key.lower() == name:
                return self.data[key]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        current_date = datetime.now()
        end_of_week = current_date + timedelta(days=7)
        birthdays_exist = False
        weekdays = {
            day: []
            for day in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        }

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_month = birthday_date.month
                birthday_day = birthday_date.day

                if birthday_month == current_date.month:
                    if (
                        current_date
                        <= datetime(current_date.year, birthday_month, birthday_day)
                        <= end_of_week
                    ):
                        day_of_week = birthday_date.strftime("%A")
                        if day_of_week in ("Saturday", "Sunday"):
                            day_of_week = "Monday"
                        weekdays[day_of_week].append(record.name.value)
                        birthdays_exist = True

        if birthdays_exist:
            return weekdays
        else:
            return "No birthdays in the upcoming week. Be happy :)"

    def load_address_book(self):
        try:
            with open("address_book.pickle", "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_address_book(self):
        with open("address_book.pickle", "wb") as file:
            pickle.dump(self.data, file)
