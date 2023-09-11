from . import address_book, note_book, file_sort

while True:
    
    choice = input('1) Address book of your victims; 2) Notebook for special murders; 3) Sort files in the current folder; 4) Exit. \nChoose program: ')
    
    try:
        choice = int(choice)
    except ValueError as error:
        print('Use only specified numbers!')

    if  choice == 1:
        address_book.main()
    elif choice == 2:
        note_book.main()
    elif choice == 3:
        file_sort.main()
    elif choice == 4:
        exit()
    else:
        print('Use only specified numbers!')