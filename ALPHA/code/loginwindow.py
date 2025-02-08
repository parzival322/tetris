def login_window():
    import tkinter as tk
    from tkinter import messagebox
    import psycopg2
    import hashlib
    from dotenv import load_dotenv
    import os

    load_dotenv()

    data = {}

    # Функция для проверки логина и пароля 
    def login(window):
        nonlocal data

        md5_hash = hashlib.new('md5')

        username = entry_username.get()

        password = entry_password.get()
        md5_hash.update(password.encode())
        md5_hex = md5_hash.hexdigest()

        conn = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), host=os.getenv('HOST'), port=os.getenv('PORT'))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE login = %s AND password = %s", (username, md5_hex)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Успешно", "Авторизация прошла успешно!")
            window.destroy()
            data = {'status': True, 'username': username}
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")


    # Функция для открытия окна регистрации
    def open_registration_window():
        registration_window = tk.Toplevel(root)
        registration_window.title("Регистрация")

        label_new_username = tk.Label(registration_window, text="Логин:")
        label_new_username.grid(row=0, column=0, padx=10, pady=10)

        entry_new_username = tk.Entry(registration_window)
        entry_new_username.grid(row=0, column=1, padx=10, pady=10)

        label_new_password = tk.Label(registration_window, text="Пароль:")
        label_new_password.grid(row=1, column=0, padx=10, pady=10)

        entry_new_password = tk.Entry(registration_window, show="*")
        entry_new_password.grid(row=1, column=1, padx=10, pady=10)

        button_register = tk.Button(
            registration_window,
            text="Зарегистрироваться",
            command=lambda: register_user(
                entry_new_username.get(), entry_new_password.get(), registration_window
            ),
        )
        button_register.grid(row=2, column=0, columnspan=2, pady=10)


    # Функция для регистрации нового пользователя
    def register_user(username, password, window):
        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль не могут быть пустыми")
            return

        conn = psycopg2.connect(dbname='selectel', user='selectel', 
                            password='selectel', host='82.202.136.203', port=5432)
        cursor = conn.cursor()
        try:

            print('Запомните свои данные:')
            print(f'login: {username}')
            print(f'password: {password}')

            md5_hash = hashlib.new('md5')
            md5_hash.update(password.encode())
            md5_hex = md5_hash.hexdigest()
            print(md5_hex)
            print(len(md5_hex))
            cursor.execute(
                'INSERT INTO users (login, password) VALUES (%s, %s)', (username, md5_hex)
            )
            conn.commit()
            messagebox.showinfo("Успешно", "Пользователь зарегистрирован!")
            window.destroy()  # Закрыть окно регистрации после успешной регистрации
        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
        finally:
            conn.close()

    
    # Создание основного окна
    root = tk.Tk()
    root.title("Окно авторизации")

    # Создание и размещение элементов интерфейса
    label_username = tk.Label(root, text="Логин:")
    label_username.grid(row=0, column=0, padx=10, pady=10)

    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(root, text="Пароль:")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    button_login = tk.Button(root, text="Войти", command=lambda: login(root))
    button_login.grid(row=2, column=0, columnspan=2, pady=10)

    button_register = tk.Button(
        root, text="Зарегистрироваться", command=open_registration_window
    )
    button_register.grid(row=3, column=0, columnspan=2, pady=10)

    # Запуск основного цикла обработки событий
    root.mainloop()

    return data