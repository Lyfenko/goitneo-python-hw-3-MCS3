from address_book import AddressBook, Record
import pickle


GREEN = '32'
CYAN = '36'
YELLOW = '33'
RED = '31'


def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Invalid command format."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return inner


class AssistantBot:
    def __init__(self):
        self.address_book = AddressBook()
        self.load_address_book()

    @staticmethod
    def greet_user():
        return "Hello! I'm your Assistant Bot. How can I assist you today?"

    def load_address_book(self):
        try:
            with open("address_book.pickle", "rb") as file:
                self.address_book.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_address_book(self):
        with open("address_book.pickle", "wb") as file:
            pickle.dump(self.address_book.data, file)

    @input_error
    def add_contact(self, name, phone, birthday=None):
        if name in self.address_book.data:
            return "Contact with this name already exists."
        if any(
            contact.name.value == name for contact in self.address_book.data.values()
        ):
            return "Contact with this name already exists."
        if any(
            contact.phones and contact.phones[0].value == phone
            for contact in self.address_book.data.values()
        ):
            return "Contact with this phone number already exists."

        record = Record(name)
        record.add_phone(phone)
        if birthday:
            record.add_birthday(birthday)
        self.address_book.add_record(record)
        return "Contact added."

    @input_error
    def find_contact(self, name):
        found_record = self.address_book.find(name)
        if found_record:
            return str(found_record)
        return "No matching records found."

    @input_error
    def delete_contact(self, name):
        if name in self.address_book.data:
            del self.address_book.data[name]
            return "Record removed."
        return "Record not found."

    @input_error
    def show_all_contacts(self):
        if self.address_book.data:
            return "\n".join(
                [str(record) for record in self.address_book.data.values()]
            )
        return "No records in the address book."

    @input_error
    def edit_contact_phone(self, name, operation, old_phone=None, new_phone=None):
        found_record = self.address_book.find(name)
        if not found_record:
            return "No matching records found."

        if operation == "Add":
            if any(
                contact.phones and contact.phones[0].value == new_phone
                for contact in self.address_book.data.values()
            ):
                return "Contact with this phone number already exists."
            found_record.add_phone(new_phone)
            self.save_address_book()
            return "Phone added."
        elif operation == "Remove":
            found_record.remove_phone(old_phone)
            self.save_address_book()
            return "Phone removed."
        elif operation == "Edit":
            if any(
                contact.phones and contact.phones[0].value == new_phone
                for contact in self.address_book.data.values()
            ):
                return "Contact with this phone number already exists."
            found_record.edit_phone(old_phone, new_phone)
            self.save_address_book()
            return "Phone edited."
        else:
            return "Invalid phone operation."

