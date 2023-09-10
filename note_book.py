import json
import os

class Note:

    def __init__(self, title, content, tags=[]):

        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"

class InvalidFormatError(Exception):
    pass

class Notebook:

    def __init__(self, filename="notes.json"):
        self.notes = []
        self.filename = filename
        #self.load_notes()

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)
        else:
            self.load_notes()


    def add_note(self, note):
            """if len(note.title) < 5:
                raise InvalidFormatError("Invalid format. Title >= 5.")
            if len(note.content) < 20:
                raise InvalidFormatError("Invalid format. Content >= 20.")"""
            if any(len(tag) > 20 for tag in note.tags):
                raise InvalidFormatError("Invalid format. Tags <= 20")
        
            # Перевірка на однакові назви
            title = note.title.casefold()
            for existing_note in self.notes:
                if existing_note.title.casefold() == title:
                    print("Note with the same title already exists.")
                    return
            
            self.notes.append(note)
            print("Note added!")


    def search_notes(self, keyword):
        """Пошук нотаток за ключовим словом."""
        keyword = keyword.lower()  # Перетворити ключове слово до нижнього регістру для нечутливого до регістру пошуку.
        matching_notes = []
        for note in self.notes:
            if keyword in note.title.lower() or keyword in note.content.lower() or keyword in note.tags:
                matching_notes.append(note)
        return matching_notes

    def find_note(self, title):
        title = title.casefold()
        for note in self.notes:
            if note.title.casefold() == title:
                return note
        return None

    def edit_note(self, title):
        note = self.find_note(title)
        if note is None:
            print("Note not found!")
            return False

        print(f"Editing note: {note.title}")
        print(f"Current content: {note.content}")

        new_content = input("Enter the new content: ")
        note.content = new_content
        print("Note edited!")
        return True
    
    def delete_note(self, title):
        title = title.casefold()
        for note in self.notes.copy():
            if note.title.casefold() == title.casefold():
                self.notes.remove(note)
                return True
        return False
    
    def sort_notes_by_tags(self, tag):
        tag = tag.casefold()
        sorted_notes = []

        for note in self.notes:
            if tag in [t.casefold() for t in note.tags]:
                sorted_notes.append(note)

        sorted_notes.sort(key=lambda x: x.title.casefold())
        return sorted_notes


    def list_notes(self):
        if not self.notes:
            print("No notes available.")
        else:
            for i, note in enumerate(self.notes, start=1):
                print(f"{i}. Title: {note.title}")
                print(f"   Content: {note.content}")
                print(f"   Tags: {', '.join(note.tags)}")

    def save_notes(self):
        data = [{'title': note.title, 'content': note.content, 'tags': note.tags} for note in self.notes]
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def load_notes(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
            self.notes = [Note(note['title'], note['content'], note['tags']) for note in data]



def main():
    filename = "notes.json"
    notebook = Notebook(filename)
    notebook.load_notes()

    while True:

        print("\nNotebook Menu:")
        print("1. Add Note(Додати нот)")
        print("2. Edit Note(Редагувати вміст)")
        print("3. Delete Note(Видалити)")
        print("4. Add Tag(Додати тег)")
        print("5. Sort Notes(Сортування)")
        print("6. List Notes(Вивести список)")
        print("7. Search Notes(Пошук)")
        print("8. loaded Notes(Завантаження)")
        print("9. saved Notes(Зберігання)")
        print("10. Exit")


        choice = input('Please select one of the options: ')

        
        if choice == '1':       
            # Додати нотатку.    
            title = input("Enter Title: ")
            try:
                if len(title) < 5:
                    raise InvalidFormatError("Invalid format. Title >= 5.")
                content = input("Enter content: ")
                if len(content) < 20:
                    raise InvalidFormatError("Invalid format. Content >= 20.")
                tags = input("Enter Tags (comma-separated or space-separated): ")
                tags = [tag.strip() for tag in tags.replace(',', ' ').split()]
                note = Note(title, content, tags)
                notebook.add_note(note)
            except InvalidFormatError as e:
                print(f"Error: {e}")

                        
        elif choice == '2':
          
            # Редагувати нотатку.
            title = input("Enter the title of the note to edit: ")

            if notebook.edit_note(title):
                print("Note edited !")

                
        elif choice == '3':
            # Видалити нотатку.
            title = input("Enter the title of the note to delete: ").strip()
            if notebook.delete_note(title.casefold()):
                print("Note deleted!")
            else:
                print("Note not found!")

                
        elif choice == '4':
              
            # Додати тег до нотатки.
            title = input("Enter the title of the note to add a tag: ")
            note = notebook.find_note(title)
            
            if note is None:
                print("Note not found!")
            else:
                new_tags_input = input("Enter the new tags (comma-separated or space-separated): ")
                new_tags = [tag.strip() for tag in new_tags_input.replace(',', ' ').split()]
                if not new_tags:
                    print("Invalid format. Tags can't be empty.")
                elif all(len(tag) < 20 for tag in new_tags):
                    if any(tag.casefold() in note.tags for tag in new_tags):
                        print("Some tags already exist for this note.")
                    else:
                        note.tags.extend(new_tags)
                        print("Tags added!")
                else:
                    print("Invalid format. Tags <= 20.")
                
                    
        elif choice == '5':
          
            # Сортування нотаток за ключовим словом.
            keyword = input("Enter a keyword to sort notes by: ")
            notes_with_keyword = [
                (note, keyword in note.title or keyword in note.content) for note in notebook.notes]
            sorted_notes = sorted(notes_with_keyword,
                                  key=lambda x: x[1], reverse=True)
            for note, _ in sorted_notes:
                print(note)

                
        elif choice == '6':
          
            # Вивести список нотаток.
            notebook.list_notes()

            
        elif choice == '7':
          
            # Пошук нотаток за ключовим словом.
            keyword = input("Enter the keyword to search notes by: ")
            matching_notes = notebook.search_notes(keyword)
            if matching_notes:
                print("Found notes:")
                for note in matching_notes:
                    print(note)
            else:
                print("No notes found.")

        elif choice == '8':
            filename = input("Enter the filename for loading notes (e.g., notes.json): ")
            notebook = Notebook(filename)
            print("Notes loaded from the file.")

        elif choice == '9':
            notebook.save_notes()
            print("Notes saved to the file.")
           
        elif choice == '10':
            notebook.save_notes()
            print("Notes saved to the file.")
            print("Bye...")
            break
            
        else:
            print('I do not understand the command!')

if __name__ == "__main__":

    main()
