"""зберігати нотатки з текстовою інформацією
проводити пошук за нотатками"""

class Note():
    def __init__(self, title, content, tags=[]):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []  # Використовуємо `None`, а не пустий список за замовчуванням

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"
    
class Notebook():
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

    def search_notes(self, keyword):
        """Пошук нотаток за ключовим словом."""
        matching_notes = []
        for note in self.notes:
            # Перевіряємо, чи містить нотатка ключове слово у заголовку або вмісті
            if keyword in note.title or keyword in note.content:
                matching_notes.append(note)
        return matching_notes

if __name__ == "__main__":
    assistant = Notebook()