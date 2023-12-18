import sqlite3



class LibraryDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('library.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           author TEXT NOT NULL,
                           quantity INTEGER NOT NULL)''')

        cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
                       ('Капитанская дочка', 'Александр Сергеевич Пушкин', 5))
        cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
                       ('Война и мир', 'Лев Николаевич Толстой', 3))

        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL)''')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('user', '12345', 'user'))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('admin', 'admin123', 'admin'))

        self.connection.commit()

    def validate_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return user[3] 
        else:
            return None

    def get_books(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()

    def add_book(self, title, author, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
                       (title, author, quantity))
        self.connection.commit()

    def update__password_admin(self, password, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (password, name))
        self.connection.commit()
    def update__name_admin(self, new_name, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, name))
        self.connection.commit()
    def update_user_name(self, name, new_name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, name))
        self.connection.commit()
    def update_book_quantity(self, book_id, new_quantity):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE books SET quantity = ? WHERE id = ?", (new_quantity, book_id))
        self.connection.commit()
    def delete_books(self,book_ids):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM books WHERE id >0",(book_ids))
        self.connection.commit()
    def delete_book(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.connection.commit()


class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} - {self.author} ({self.quantity} шт.)"


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Library:
    def __init__(self, database):
        self.database = database
        self.current_user = User('','','')

    def login(self, username, password):
        role = self.database.validate_user(username, password)
        if role:
            self.current_user = User(username, password, role)
            print('Авторизация успешна.')
        else:
            print('Ошибка авторизации.')


    def change_password_admin(self, new_password, name):
        if self.current_user.role == 'admin':
            self.database.update__password_admin(new_password, name)
            print('Книга успешно добавлена в библиотеку.')
        else:
            print('Ошибка доступа. Добавлять книги может только администратор.')

    def add_book(self, title, author, quantity):
        if self.current_user.role == 'admin':
            self.database.add_book(title, author, quantity)
            print('Книга успешно добавлена в библиотеку.')
        else:
            print('Ошибка доступа. Добавлять книги может только администратор.')

    def delete_books(self,book_ids):
            self.database.delete_books(book_ids)
            print('Книга успешно удалена из библиотеки.')


    def delete_book(self, book_id):
        if self.current_user.role == 'admin':
            self.database.delete_book(book_id)
            print('Книга успешно удалена из библиотеки.')
        else:
            print('Ошибка доступа. Удалять книги может только администратор.')

    def show_books(self):
        books = self.database.get_books()
        for book in books:
            book_obj = Book(book[1], book[2], book[3])
            print(book_obj)

    def update_book_quantity(self, book_id, new_quantity):
        if self.current_user.role == 'admin':
            self.database.update_book_quantity(book_id, new_quantity)
            print('Количество книг успешно обновлено.')
        else:
            print('Ошибка доступа. Обновлять количество книг может только администратор.')


database = LibraryDatabase()

c = 2
book_ids = 0
library = Library(database)
print("Введите ваш ник:")
name = input()
print("Введите ваш пароль:")
passward = input()
library.login(name, passward)
while True:
    if(name == "admin"):
        print("Что вы хотите сделать?")
        print("1. Изменить свое имя")
        print("2. Изменить пароль пользователя")
        print("3. Удалить книги из реестра")
        print("4. Добавить книги в реестр")
        print("5. Выйти")


        answer = input("Введите номер команды: ")
        match answer:
            case "1":
                print("Введите новый пароль")
                new_passward = input()
                library.change_password_admin(new_passward,name)
            case "2":  
                continue
            case "3":
                for i in range(c,book_ids):
                    library.delete_books(i)
                continue
            case "4":
                library.add_book('Преступление и наказание', 'Федор Михайлович Достоевский', 10)
                c=c+1
                book_ids = c
                continue
            case "5":
                for i in range(c,book_ids):
                    library.delete_books(i)
                break
            case _:
                print("Такой команды нету!")
    
    library.show_books()


    library.update_book_quantity(1, 8)


    library.delete_book(2)