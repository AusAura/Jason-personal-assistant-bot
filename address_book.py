from collections import UserDict
from datetime import datetime, timedelta
import json
import re


class TerribleException(Exception):
    pass


class ExcessiveArguments(Exception):
    pass


class WrongArgumentFormat(Exception):
    pass


def command_phone_operations_check_decorator(func):
    def inner(*args, **kwargs) -> None:

        try:
            func(*args, **kwargs)

        except TypeError as error:
            print('Argument type is not acceptable!', error)
            return
        except ValueError as error:
            print(
                f'Too many arguments for {func.__name__}! Probably you are using too many spaces.', error)
            return
        except IndexError as error:
            print(f'Not enough arguments for {func.__name__}!', error)
            return
        except TerribleException as error:
            print('''Something REALLY unknown had happened during your command reading! Please stay  
            calm and run out of the room!''', error)
            return
        except KeyError as error:
            print('Such command (or object) does not exist!', error)
            return
        except ExcessiveArguments as error:
            print(
                f'Too many arguments for {func.__name__}! Probably you are using too many spaces.', error)
            return
        except WrongArgumentFormat:
            return

    return inner


class AddressBook(UserDict):
    N_LIMIT = 2

    def __init__(self):
        super().__init__()
        self.count = 0
        self.call_List = list(self.data.keys())
        with open('Untitled/file_address_book.json') as reader:
            try:
                file_data = json.load(reader)
                for item in file_data:
                    name = Name(item['name'])
                    random_var = item['Phone number']
                    row_email = Email(item['email'])
                    row_address = Address(item['address'])
                    record = Record(name,
                                    random_var[0], row_email, row_address)
                    iter = 1
                    while iter < len(random_var):
                        record.add_phone(
                            random_var[iter])
                        iter += 1
                    record.set_birthday(item['Date of birth'])
                    self.data[item['name']] = record
            except json.decoder.JSONDecodeError:
                file_data = []
        # print(self.data)

    def add_record(self, record, *_):
        self.data.update({record.name.value: record})

    def delete_record(self, contact_name):
        if str(contact_name) in self.data:
            del self.data[str(contact_name)]
            return None

    def close_record_data(self):
        file_data = []
        print(self.data)
        for record in self.data.values():
            write_dict = {}
            write_dict["name"] = record.name.value
            write_dict["Phone number"] = [str(ph) for ph in record.phones]
            write_dict["Date of birth"] = record.birthday.value.strftime(
                "%d %B %Y") if record.birthday else ''
            write_dict["email"] = str(
                record.email) if record.email else ''
            write_dict["address"] = str(
                record.address) if record.address else ''
            file_data.append(write_dict)
        with open('Untitled/file_address_book.json', 'w') as writer:
            json.dump(file_data, writer, indent=4)

    def iterator(self, n):
        counter = 0

        if n > len(self.data):
            n = len(self.data)
            print(
                f'Seems like there is only {len(self.data)} items in the book!')
            counter = len(self.data) + 1

        for key, value in self.data.items():
            print(key, value)
            counter += 1

            if counter == n:
                counter = 0
                yield

        print('This was the end of the address book!')
        return


class Record:

    def __init__(self, name, phone, email_value=None, address_value=None):
        self.name = name
        self.phones = []
        self.phones.append(phone)
        self.email = None
        self.address = None

        if email_value:
            self.email = Email('')
            self.email = email_value  # add email if not empty

        if address_value:
            self.address = Address('')
            self.address = address_value

        self.birthday = None

    def __repr__(self):
        return f"{self.name}; {self.phones}; {self.birthday if self.birthday else ''}; {self.email if self.email else ''}; {self.address if self.address else ''}"

    def add_phone(self, phone):
        new_phone = Phone('')
        new_phone.value = phone
        if new_phone.value not in [ph for ph in self.phones]:
            self.phones.append(new_phone)
            print(
                f'{new_phone} record was successfully added for {self.name.value}')
        else:
            print(
                f'{new_phone} is already actually recorded in {self.name.value}')

    def edit_phone(self, old_phone):

        new_phone_value = ''

        for phone in self.phones:

            if phone.value == old_phone:
                new_phone_value = input('Please input the new phone number: ')
                phone.value = new_phone_value
                break

        return new_phone_value

    def delete_phone(self, phone):

        for index, record in enumerate(self.phones, 0):
            if record.value == phone:
                self.phones.pop(index)
                print(f'{phone} was successfully deleted for {self.name.value}')
                return

        print('No such phone record!')

    def _days_to_birthday(self):

        if self.birthday is None:
            print(f'BDay record is not set for {self.name.value}!')
            return

        days_left = self.birthday._days_to_birthday()
        print(
            f'{self.name.value}\'s birthday will be roughly in {days_left} days! ({self.birthday.value.strftime("%d %B %Y")})')

    def set_birthday(self, date_val):
        self.birthday = Birthday('')
        self.birthday.value = date_val
        print(f'{self.birthday} BDay record was added for {self.name.value}!')

    def set_email(self, email_val):
        self.email.value = email_val
        print(f'{self.email} email record was added for {self.name.value}!')


class Field:

    def __init__(self, value):
        self._value = value

    def __repr__(self) -> str:
        return f'{self._value}'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Birthday(Field):

    def __init__(self, value):
        self.__value = value  # from 10 January 2020

    def _days_to_birthday(self):

        datenow = datetime.now().date()
        future_bday_date = datetime(
            year=datenow.year, month=self.value.month, day=self.value.day).date()

        if future_bday_date < datenow:
            future_bday_date = datetime(
                year=datenow.year + 1, month=self.value.month, day=self.value.day).date()

        delta = future_bday_date - datenow
        pure_days = delta.days % 365
        return pure_days

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):

        try:
            self.__value = datetime.strptime(new_value, '%d %B %Y').date()
        except ValueError:
            print(
                'Your data format is not correct! Please use this one: "10 January 2020"')
            raise WrongArgumentFormat

    def __repr__(self) -> str:
        return f'{self.value.strftime("%d %B %Y")}'


class Name(Field):

    def __init__(self, value):
        self._value = value

    def __repr__(self) -> str:
        return f'{self._value}'


class Phone(Field):

    def __init__(self, value):
        self.__value = value

    def __repr__(self) -> str:
        return f'{self.__value}'

    @property
    def value(self):
        return self.__value

    @staticmethod
    def valid_phone(phone: str):
        if 10 <= len(phone) <= 13:
            if phone.replace('+', ' ').isdigit():
                return True
            return False
        else:
            return False

    @staticmethod
    def convert_phone_number(phone: str):

        correct_phone_number = ''

        if phone.startswith('+380') and len(phone) == 13:
            correct_phone_number = phone
        elif phone.startswith('80') and len(phone) == 11:
            correct_phone_number = '+3' + phone
        elif phone.startswith('0') and len(phone) == 10:
            correct_phone_number = '+38' + phone
        else:
            print('Number format is not correct! Must contain 10-13 symbols and must match the one of the current '
                  'formats: +380001112233 or 80001112233 or 0001112233')
            raise WrongArgumentFormat

        return correct_phone_number

    @value.setter
    def value(self, new_value):
        is_valid = self.valid_phone(new_value)
        if is_valid:
            self.__value = self.convert_phone_number(new_value)
        else:
            print('Number format is not correct! Must contain 10-13 symbols and must match the one of the current '
                  'formats: +380001112233 or 80001112233 or 0001112233')
            raise WrongArgumentFormat


class Email(Field):

    def __init__(self, value):
        self.__value = value

    def __repr__(self) -> str:
        return f'{self.__value}'

    @property
    def value(self):
        return self.__value

    @staticmethod
    def valid_email(email: str):
        if re.match(
            r'^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}\.[a-z]{2,3}$', email) or re.match(
                r"^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}$", email):
            return True
        return False

    @value.setter
    def value(self, new_value):
        is_valid = self.valid_email(new_value)
        if is_valid:
            self.__value = new_value
        else:
            print('The email address is not valid! Must contain min 2 characters before "@" and 2-3 symbols in TLD! '
                  'Example: aa@example.net or aa@example.com.ua')
            raise WrongArgumentFormat


class Address(Field):

    def __init__(self, value):
        self.__value = value

    def __repr__(self):
        return f"{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


def deconstruct_command(input_line: str) -> list:
    line_list = input_line.split(' ')

    if len(line_list) <= 0:
        print('''Something REALLY unknown had happened during your command reading! Please stay  
              calm and run out of the room!''')
        return

    if len(line_list) == 1:
        return line_list

    old_complex_command = line_list[0].casefold()
    new_line_list = line_list.copy()

    for item in line_list:

        if item.casefold() == old_complex_command:
            new_line_list.remove(item)
            continue

        new_complex_command = old_complex_command + ' ' + item.casefold()

        if new_complex_command not in command_list:
            new_line_list.insert(0, old_complex_command)
            break

        new_line_list.remove(item)
        old_complex_command = new_complex_command

        if len(new_line_list) == 0:
            new_line_list.insert(0, old_complex_command)
            break

    return new_line_list


def load():
    adr_book = AddressBook()

    try:
        with open('save.json', 'r') as json_file:
            data = json.load(json_file)

            for record_data in data:
                row_name = Name(record_data['Name'])
                row_birthday = Birthday(record_data['Birthday'])
                row_email = Email(record_data['Email'])
                row_address = Address(record_data['Address'])
                record = Record(row_name, '', row_email, row_address)

                row_phones = record_data['Phones']

                if row_phones:

                    row_normalized_phones = row_phones.split(',')
                    row_serialized_phones = [
                        Phone(phone) for phone in row_normalized_phones]

                else:
                    row_serialized_phones = ''

                record.phones = row_serialized_phones
                record.birthday = row_birthday
                adr_book.add_record(record)

    except FileNotFoundError:
        print('Have not found created address book. Nothing to load from.')

    return adr_book


def save(adr_book):
    data = []

    for record in adr_book.data.values():
        record_data = {
            'Name': record.name.value,
            'Phones': [phone.value for phone in record.phones],
            'Email': record.email.value,
            'Address': record.address.value,
            'Birthday': record.birthday.value
        }
        data.append(record_data)

    try:
        with open('save.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print('The data is saved in JSON format.')

    except FileNotFoundError:
        print('Data could not be saved. Check the path to the file.')


@command_phone_operations_check_decorator
def perform_command(command: str, adr_book, *args, **kwargs) -> None:
    command_list[command](adr_book, *args, **kwargs)


# curry functions
@command_phone_operations_check_decorator
def add_record(adr_book, line_list):
    if len(line_list) > 5:
        raise ExcessiveArguments

    name = Name(line_list[1])
    phone_number = Phone('')
    phone_number.value = line_list[2]

    try:
        line_list[3]
    except IndexError:
        email = Email('')
    else:
        email = Email('')
        email.value = line_list[3]  # add Email from list

    try:
        line_list[4]
    except IndexError:
        address = Address('')
    else:
        address = Address('')
        address.value = line_list[4]

    record = Record(name, phone_number, email, address)
    adr_book.add_record(record)
    print(
        f'Added record for {name.value} with {phone_number.value}, email \'{email.value}\', and address \'{address.value}\' my lord.')


@command_phone_operations_check_decorator
def add_phone(adr_book, line_list):
    if len(line_list) > 3:
        raise ExcessiveArguments

    record_name = line_list[1]
    phone = line_list[2]

    try:
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return

    adr_book.data[record_name].add_phone(phone)


@command_phone_operations_check_decorator
def edit_phone(adr_book, line_list) -> None:
    if len(line_list) > 3:
        raise ExcessiveArguments

    try:
        record_name = line_list[1]
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return

    old_phone = line_list[2]
    new_phone = adr_book.data[record_name].edit_phone(old_phone)

    if new_phone:
        print(f'{old_phone} was successfully changed to {new_phone} for {record_name}')
    else:
        print(f'{old_phone} phone number was not found for {record_name}!')


@command_phone_operations_check_decorator
def delete_phone(adr_book, line_list) -> None:
    if len(line_list) > 3:
        raise ExcessiveArguments

    record_name = line_list[1]
    phone = line_list[2]

    try:
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return

    adr_book.data[record_name].delete_phone(phone)


@command_phone_operations_check_decorator
def delete_record(adr_book, line_list):
    if len(line_list) > 3:
        raise ExcessiveArguments
    if line_list[1] in adr_book.data:
        name = Name(line_list[1])
        adr_book.delete_record(name)
        print(f'Removed record for {line_list[1]}, my lord.')
    else:
        print("No such phone record!")


def close_without_saving(*_):
    print('Will NOT save! BB!')
    exit()


@command_phone_operations_check_decorator
def find(adr_book, line_list):
    if len(line_list) > 3:
        raise ExcessiveArguments

    str_to_find = line_list[1]
    is_empty = True
    print(f'Looking for {str_to_find}. Found...')

    for record in adr_book.data.values():

        if record.name.value.find(str_to_find) != -1:
            is_empty = False
            print(record.name, record, record.birthday.value)
            continue

        for phone in record.phones:

            if phone.value.find(str_to_find) != -1:
                is_empty = False
                print(record.name, record, record.birthday.value)
                break

    if is_empty:
        print('Nothing!')


def finish_session(adr_book, *_) -> None:
    adr_book.close_record_data()
    print('Good bye!')
    exit()


def hello(*_) -> None:
    print('How can I help you?')


def help(*_):
    print(command_list.keys())


@command_phone_operations_check_decorator
def show_all_items(adr_book, *_) -> None:
    if bool(adr_book.data) == False:
        print('Your list is empty!')
        return

    for record in adr_book.data:
        if bool(adr_book.data[record].phones) == False:
            print(f'Your list for {record} is empty!')
            continue

        print(f'Phones for {record}:')
        for id, phone in enumerate(adr_book.data[record].phones, 1):
            print(f'{id}) - {phone}')

        # if bool(adr_book.data[record].phones) == False:
        #     print(f'Your list for {record} is empty!')
        #     continue

        # print(f'Phones for {record}:')
        # for id, phone in enumerate(adr_book.data[record].phones, 1):
        #     print(f'{id}) - {phone.value}')


@command_phone_operations_check_decorator
def show_bday_in_days(adr_book, *_) -> None:

    days_timeframe = input(
        'In how many days you want to see BDays of your victims? ')
    print('*' * 10)
    datetime_timedelta = timedelta(days=int(days_timeframe))
    is_empty = True

    print(f'You wanted to see Bdays in {days_timeframe} days! Here we go: ')

    for record in adr_book.data.values():

        record_timedelta = timedelta(days=record.birthday._days_to_birthday())

        if record_timedelta <= datetime_timedelta:
            print('=' * 10)
            print(
                f'{record.name} will have a BDay in {record_timedelta.days}! ({record.birthday})')
            print(f'His data: {record.phones}, {record.email}')

            is_empty = False

    if is_empty:
        print('Sorry! Seems like nobody have BDays in the set timeframe!')


@command_phone_operations_check_decorator
def show_some_items(adr_book, *_):
    n = input('How much records to show at a time? ')
    iterator = adr_book.iterator(int(n))
    try:
        next(iterator)
    except StopIteration:
        return

    while True:

        action = input('Show next part? (Y/N): ').casefold()

        if action == 'y':
            try:
                next(iterator)
            except StopIteration:
                return
        elif action == 'n':
            return
        else:
            print('I do not understand the command!')


@command_phone_operations_check_decorator
def set_email(adr_book, line_list, *_):

    record_name = line_list[1]

    try:
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return

    email_val = input('Please set the email like "myemail@google.com": ')

    if email_val:
        adr_book.data[record_name].set_email(email_val)


@command_phone_operations_check_decorator
def set_birthday(adr_book, line_list, *_):
    record_name = line_list[1]

    try:
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return

    date_val = input('Please set the birthday date like "10 January 2020": ')
    adr_book.data[record_name].set_birthday(date_val)


@command_phone_operations_check_decorator
def set_address(adr_book, line_list, *_):

    record_name = line_list[1]

    try:
        adr_book.data[record_name]
    except KeyError:
        print(f'Cannot find name {record_name} in the list!')
        return
    address_val = input('Please set the address: ')
    adr_book.data[record_name].address = address_val
    print(f'Address {address_val} was set successfully for {record_name}!')


@command_phone_operations_check_decorator
def show_email(adr_book, line_list, *_):
    record_name = line_list[1]

    if adr_book.data[record_name].email.value:
        print(f'It is {adr_book.data[record_name].email}')
    else:
        print('It is EMPTY!')


@command_phone_operations_check_decorator
def show_birthday(adr_book, line_list, *_):
    record_name = line_list[1]
    adr_book.data[record_name]._days_to_birthday()


@command_phone_operations_check_decorator
def show_address(adr_book, line_list, *_):

    record_name = line_list[1]
    address = adr_book.data[record_name].address

    if address:
        print(f"Address for {record_name}: {address}")
    else:
        print(f"No address is set for {record_name}")


command_list = {'not save': close_without_saving,
                'good bye': finish_session,
                'close': finish_session,
                'hello': hello,
                'add': add_record,
                'add phone': add_phone,
                'edit phone': edit_phone,
                'show all': show_all_items,
                'show some': show_some_items,
                'delete phone': delete_phone,
                'delete contact': delete_record,
                'set bday': set_birthday,
                'set email': set_email,
                'set address': set_address,
                'show bday': show_birthday,
                'show email': show_email,
                'show address': show_address,
                'find': find,
                'help': help,
                'bday in': show_bday_in_days}


# main
def main():

    # adr_book = load()
    adr_book = ab
    help()

    while True:

        print('*' * 10)
        input_line = input('Put your request here: ')

        line_list = deconstruct_command(input_line)
        current_command = line_list[0].casefold()

        perform_command(current_command, adr_book, line_list)


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    email = Email('')
    adress = Address('')
    adress = '40 street 122, 55'
    print(adress)
    rec = Record(name, phone, email, adress)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    rec.set_birthday('10 January 2020')
    rec.set_email('test@gmail.com')
    print(ab['Bill'].birthday)

    name = Name('John')
    phone = Phone('1234567890')
    email = Email('')
    adress = Address('')
    adress = '40 street 122, 55'
    rec = Record(name, phone, email, adress)
    rec.set_birthday('10 September 2020')
    rec.set_email('test@gmail.com')
    ab.add_record(rec)

    name = Name('Mike')
    phone = Phone('1234567890')
    email = Email('')
    adress = Address('')
    adress = '40 street 122, 55'
    rec = Record(name, phone, email, adress)
    rec.set_birthday('10 July 2020')
    rec.set_email('test@gmail.com')
    ab.add_record(rec)

    print('All Ok)')

    main()
