from assistant_bot import AssistantBot


def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


GREEN = '32'
CYAN = '36'
YELLOW = '33'
RED = '31'


def main():
    assistant = AssistantBot()
    print("Welcome to the Assistant Bot!")

    while True:
        print("Commands:")
        print("1. Add contact")
        print("2. Find contact by name")
        print("3. Delete contact")
        print("4. Show all contacts")
        print("5. Edit contact phone (Add/Remove/Edit)")
        print("6. Show upcoming birthdays")
        print("7. Exit")
        print("Type 'hello' to be greeted by the bot.")
        print("Type 'help' for command descriptions.")

        choice = input("Enter your choice: ")

        if choice.lower() == "hello":
            print(colorize(f"Assistant Bot: {assistant.greet_user()}", GREEN))
        elif choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            birthday = input("Enter birthday (DD.MM.YYYY, optional): ")
            result = assistant.add_contact(name, phone, birthday)
            print(colorize(f"Assistant Bot: {result}", CYAN))
        elif choice == "2":
            name = input("Enter name to search: ")
            result = assistant.find_contact(name)
            print(colorize(f"Assistant Bot: {result}", CYAN))
        elif choice == "3":
            name = input("Enter name to remove: ")
            result = assistant.delete_contact(name)
            print(colorize(f"Assistant Bot: {result}", CYAN))
        elif choice == "4":
            result = assistant.show_all_contacts()
            print(colorize(f"Assistant Bot: {result}", CYAN))
        elif choice == "5":
            name = input("Enter name to edit phone: ")
            phone_choice = input("Choose an option (Add/Remove/Edit): ")
            if phone_choice in ["Add", "Remove", "Edit"]:
                if phone_choice == "Add":
                    new_phone = input("Enter the new phone number: ")
                    result = assistant.edit_contact_phone(name, phone_choice, new_phone=new_phone)
                elif phone_choice == "Remove":
                    old_phone = input("Enter the phone number to remove: ")
                    result = assistant.edit_contact_phone(name, phone_choice, old_phone=old_phone)
                else:
                    old_phone = input("Enter the old phone number: ")
                    new_phone = input("Enter the new phone number: ")
                    result = assistant.edit_contact_phone(name, phone_choice, old_phone=old_phone, new_phone=new_phone)
                print(colorize(f"Assistant Bot: {result}", CYAN))
            else:
                print(colorize("Assistant Bot: Invalid phone operation.", RED))
        elif choice == "6":
            birthdays = assistant.address_book.get_birthdays_per_week()
            if isinstance(birthdays, str):
                print(colorize(f"Assistant Bot: {birthdays}", CYAN))
            else:
                print(colorize("Assistant Bot: Upcoming birthdays:", CYAN))
                for day, names in birthdays.items():
                    if names:
                        print(colorize(f"{day}:{', '.join(names)}", YELLOW))
        elif choice == "7":
            print("Goodbye!")
            assistant.save_address_book()
            break
        elif choice.lower() == "help":
            print("Help:")
            print("1. Add contact: Add a new contact with name, phone, and optional birthday.")
            print("2. Find contact by name: Find a contact by their name.")
            print("3. Delete contact: Delete a contact by name.")
            print("4. Show all contacts: Show all contacts in the address book.")
            print("5. Edit contact phone (Add/Remove/Edit): Edit a contact's phone number.")
            print("6. Show upcoming birthdays: Show upcoming birthdays for the next week.")
            print("7. Exit: Close the program.")
        else:
            print(colorize("Assistant Bot: Invalid command. Type 'help' for command descriptions.", RED))


if __name__ == "__main__":
    main()
