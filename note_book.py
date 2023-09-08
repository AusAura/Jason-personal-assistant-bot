"""зберігати нотатки з текстовою інформацією
проводити пошук за нотатками"""

class Note:
  
    def __init__(self, title, content, tags=[]):
      
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []  # Використовуємо `None`, а не пустий список за замовчуванням

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"

class Notebook:
  
    def __init__(self):
        # Список для зберігання нотаток
        self.notes = []

    def add_note(self, note):
        """Додати нотатку до списку."""
        # Перевіряємо, чи існує нотатка з такою самою назвою
        
        if isinstance(note, Note):
            for existing_note in self.notes:
              
                if existing_note.title == note.title:
                    print("Нотатка з такою назвою вже існує.")
                    return
                  
            self.notes.append(note)
            print("Нотатка збережена.")
            
        else:
            print("Помилка: Нотатка має бути об'єктом класу Note.")    

    def edit_note(self, title, new_content):
      
        for note in self.notes:
          
            if note.title == title:
                note.content = new_content
                return True
              
        return False

    def delete_note(self, title):
      
        for note in self.notes:
          
            if note.title == title:
                self.notes.remove(note)
                return True
              
        return False
      
    def search_notes(self, keyword):
      
        """Пошук нотаток за ключовим словом."""
        matching_notes = []
        
        for note in self.notes:
            # Перевіряємо, чи містить нотатка ключове слово у заголовку або вмісті
            
            if keyword in note.title or keyword in note.content:
                matching_notes.append(note)
                
        return matching_notes     

      
def main():
  
    notebook = Notebook()
    
    while True:
      
        print("\nNotebook Menu:")
        print("1. Add Note(Додати)")
        print("2. Edit Note(Редагувати)")
        print("3. Delete Note(Видалити)")
        print("4. Sort Notes(Сортування)")
        print("5. Exit")

        choice = input("Enter command >>> ")

        if choice == '1':
            # Додати нотатку.
            title = input("Enter the title: ")
            content = input("Enter the content: ")
            tags = input("Enter tags: ").split(', ')
            note = Note(title, content, tags)
            notebook.add_note(note)
            print("Note added successfully!")
            
        elif choice == '2':
            # Редагувати нотатку.
            title = input("Enter the title of the note to edit: ")
            new_content = input("Enter the new content: ")
            
            if notebook.edit_note(title, new_content):
                print("Note edited successfully!")
                
            else:
                print("Note not found!")

        elif choice == '3':
            # Видалити нотатку.
            title = input("Enter the title of the note to delete: ")
            
            if notebook.delete_note(title):
                print("Note deleted successfully!")
                
            else:
                print("Note not found!")

        elif choice == '4':
            # Сортування нотаток за ключовим словом.
            keyword = input("Enter a keyword to sort notes by: ")
            # Створюємо список.
            notes_with_keyword = [(note, keyword in note.title or keyword in note.content) for note in notebook.notes]
            # Сортуємо список(спочатку нотатки з ключовим словом).
            sorted_notes = sorted(notes_with_keyword, key=lambda x: x[1], reverse=True)
            # Виводимо.           
            for note, _ in sorted_notes:
                print(note)

        elif choice == '5':
            print("Bye...")
            break

if __name__ == "__main__":
    main()