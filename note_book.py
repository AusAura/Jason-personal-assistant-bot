class Note:
  
    def __init__(self, title, content, tags=[]):
      
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else [] 

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"

class Notebook:
  
    def __init__(self):
        self.notes = []

    def add_note(self, note):
            title = note.title.casefold()
        #if len(note.title) >= 5 and len(note.content) >= 20 and all(len(tag) <= 5 for tag in note.tags):
            # Перевірка на однакові назви
            for existing_note in self.notes:
                if existing_note.title.casefold() == title:
                    print("Note with the same title already exists.")
                    return
            
            """# Перевірка на однакові теги
            for existing_note in self.notes:
                if any(tag in existing_note.tags for tag in note.tags):
                    print("Note with the same tag already exists.")
                    return"""
            self.notes.append(note)
            print("Note added !")
        #else:
            #print("Invalid format. Title >= 5, content >=  20,tags <= 5.")


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
        for note in self.notes:
          
            if note.title == title:
                self.notes.remove(note)
                print("Note deleted!")
                return
        print("Note not found!")
    
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

      
def main():
  
    notebook = Notebook()
    
    while True:
      
        print("\nNotebook Menu:")
        print("1. Add Note(Додати нот)")
        print("2. Edit Note(Редагувати вміст)")
        print("3. Delete Note(Видалити)")
        print("4. Add Tag(Додати тег)")
        print("5. Sort Notes(Сортування)")
        print("6. List Notes(Вивести список)")
        print("7. Exit")


        choice = input("Enter command >>> ")
        if choice == '1':
            # додати нотатку.
            title = input("Enter the title: ")
            for existing_note in notebook.notes:
                if existing_note.title.casefold() == title.casefold():
                    print("Note with the same title already exists.")
                    break
            else:
                content = input("Enter the content: ")
                tags = input("Enter tags (comma-separated or space-separated): ")
                tags = [tag.strip() for tag in tags.replace(',', ' ').split()]
                note = Note(title, content, tags)
                notebook.add_note(note)
                print("Note added successfully!")

        elif choice == '2':
            # Редагувати нотатку.
            title = input("Enter the title of the note to edit: ")
            if notebook.edit_note(title):
                print("Note edited!")

        elif choice == '3':
            # Видалити нотатку.
            title = input("Enter the title of the note to delete: ")
            notebook.delete_note(title)

        elif choice == '4':
            # Додати тег до нотатки.
            title = input("Enter the title of the note to add a tag: ")
            note = notebook.find_note(title)
            if note is None:
                print("Note not found!")
            else:
                new_tag = input("Enter the new tag: ")
                note.tags.append(new_tag)
                print("Tag added successfully!")

        elif choice == '5':
            # Сортування нотаток.
            keyword = input("Enter a keyword to sort notes by: ")
            sorted_notes = notebook.sort_notes_by_tags(keyword)
            for i, note in enumerate(sorted_notes, start=1):
                print(f"{i}. {note.title}")

        elif choice == '6':
            # Вивести список нотаток.
            notebook.list_notes()

        elif choice == '7':
            print("Bye...")
            break

if __name__ == "__main__":
    main()