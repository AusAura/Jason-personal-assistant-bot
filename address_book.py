from collections import UserDict
from datetime import datetime
import csv
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
            print(f'Too many arguments for {func.__name__}! Probably you are using too many spaces.', error)
            return
        except IndexError as error:
            print(f'Not enough arguments for {func.__name__}!', error)
            return
        except TerribleException:
            print('''Something REALLY unknown had happened during your command reading! Please stay  
            calm and run out of the room!''', error)
            return
        except KeyError as error:
            print('Such command (or object) does not exist!', error)
            return
        except ExcessiveArguments as error:
            print(f'Too many arguments for {func.__name__}! Probably you are using too many spaces.', error)
            return
        except WrongArgumentFormat:
            return

    return inner


class AddressBook(UserDict):

    def add_record(self, record, *_):
        self.data.update({record.name.value: record})

    def iterator(self, n):
        counter = 0

        if n > len(self.data):
            n = len(self.data)
            print(f'Seems like there is only {len(self.data)} items in the book!')
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

    def __init__(self, name, phone):
        self.name = name
        self.phones = []
        self.phones.append(phone)
        self.birthday = None

    def __repr__(self) -> str:
        return f'{self.phones}'

    def add_phone(self, phone):
        new_phone = Phone('')
        new_phone.value = phone
        self.phones.append(new_phone)
        print(f'{new_phone.value} record was successfully added for {self.name.value}')

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
        future_bday_date = datetime(year=datenow.year, month=self.value.month, day=self.value.day).date()

        if future_bday_date < datenow:
            future_bday_date = datetime(year=datenow.year + 1, month=self.value.month, day=self.value.day).date()

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
            print('Your data format is not correct! Please use this one: "10 January 2020"')
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

    @value.setter
    def value(self, new_value):
        if len(new_value) == 10:
            self.__value = new_value
        else:
            print('Number format is not correct! Should be: "0990002233"')
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
                    r'^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}+\.[a-z]{2,3}$', email) or re.match(
                                                            r"^[\w.+\-]{1}[\w.+\-]+@\w+\.[a-z]{2,3}$", email):
                return True
            print('The email address is not valid! Must contain min 2 characters before "@"! Example: aa@example.com '
                  'or aa@example.com.ua')
            raise ValueError

        @value.setter
        def value(self, new_value):
            valid_result = self.valid_email(new_value)
            if valid_result:
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
        with open('save.csv', newline='') as fh:
            reader = csv.DictReader(fh)

            for row in reader:

                row_name = Name(row['Name'])
                row_birthday = Birthday(row['Birthday'])
                record = Record(row_name, '')

                row_phones = row['Phones']

                if row_phones:

                    row_normalized_phones = row_phones.replace('[', '')
                    row_normalized_phones = row_normalized_phones.replace(']', '')
                    row_normalized_phones = row_normalized_phones.replace(' ', '')
                    row_normalized_phones = row_normalized_phones.split(',')

                    row_serialized_phones = [Phone(phone) for phone in row_normalized_phones]

                else:
                    row_serialized_phones = ''

                record.phones = row_serialized_phones
                record.birthday = row_birthday

                adr_book.add_record(record)

    except FileNotFoundError:
        print('Have not found created address book. Nothing to load from.')

    return adr_book


def save(adr_book):
    with open('save.csv', 'w', newline='') as fh:

        writer = csv.DictWriter(fh, fieldnames=['Name', 'Phones', 'Birthday'])
        writer.writeheader()

        try:
            for record in adr_book.data.values():
                writer.writerow({'Name': record.name, 'Phones': record.phones, 'Birthday': record.birthday.value})

        except AttributeError as error:

            print('Error writing a file, try again:', error)
            return -1


@command_phone_operations_check_decorator
def perform_command(command: str, adr_book, *args, **kwargs) -> None:
    command_list[command](adr_book, *args, **kwargs)


## curry functions
@command_phone_operations_check_decorator
def add_record(adr_book, line_list):
    if len(line_list) > 3:
        raise ExcessiveArguments

    name = Name(line_list[1])
    phone_number = Phone('')
    phone_number.value = line_list[2]
    record = Record(name, phone_number)
    adr_book.add_record(record)
    print(f'Added record for {name.value} with {phone_number.value}, my lord.')


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
    if save(adr_book) == None:
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
            print(f'{id}) - {phone.value}')


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
def show_birthday(adr_book, line_list, *_):
    record_name = line_list[1]
    adr_book.data[record_name]._days_to_birthday()


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
                'set bday': set_birthday,
                'show bday': show_birthday,
                'find': find,
                'help': help}


# main
def main():
    adr_book = load()
    help()

    while True:
        input_line = input('Put your request here: ')

        line_list = deconstruct_command(input_line)
        current_command = line_list[0].casefold()

        perform_command(current_command, adr_book, line_list)


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print('All Ok)')

    main()
