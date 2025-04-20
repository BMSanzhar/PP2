import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host="localhost",
    dbname="phonebook2_db",
    user="postgres",
    password="87277478111",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook2 (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        phone TEXT
    )
""")

# 1. Паттерн бойынша іздеу функциясы
def search_pattern(pattern):
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Username", "Phone"], tablefmt="grid"))

# 2. Бір қолданушыны енгізу немесе жаңарту процедурасы
def insert_or_update_user(username, phone):
    cur.execute("CALL insert_or_update_user(%s, %s)", (username, phone))
    conn.commit()
    print(f"✅ User {username} has been added or updated successfully!")

# 3. Көптеген қолданушыларды енгізу процедурасы
def insert_many_users(usernames, phones):
    cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
    conn.commit()
    print("✅ Users have been added successfully!")

# Меню
def menu():
    while True:
        print("\n📱 PHONEBOOK MENU:")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            pattern = input("Enter a name or phone number pattern to search: ")
            search_pattern(pattern)
        elif choice == "2":
            username = input("Enter username: ")
            phone = input("Enter phone number: ")
            insert_or_update_user(username, phone)
        elif choice == "3":
            usernames = input("Enter usernames as comma-separated values: ").split(",")
            phones = input("Enter phone numbers as comma-separated values: ").split(",")
            insert_many_users(usernames, phones)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

    cur.close()
    conn.close()
    print("Connection closed.")

# Мәзірді бастау
menu()



# ===============================
# SQL ФУНКЦИИ И ПРОЦЕДУРЫ
# ===============================

# 1. Функция для поиска по шаблону:
# ---------------------------------
# CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
# RETURNS TABLE(id INT, username TEXT, phone TEXT)
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     RETURN QUERY
#     SELECT phonebook2.id, phonebook2.username, phonebook2.phone
#     FROM phonebook2
#     WHERE phonebook2.username ILIKE '%' || pattern || '%'
#        OR phonebook2.phone ILIKE '%' || pattern || '%';
# END;
# $$;


# 2. Процедура для вставки или обновления одного пользователя:
# -------------------------------------------------------------
# CREATE OR REPLACE PROCEDURE insert_or_update_user(
#     p_username VARCHAR,
#     p_phone VARCHAR
# )
# LANGUAGE plpgsql
# AS $$
# BEGIN
#     IF EXISTS (
#         SELECT 1 FROM phonebook2 WHERE username = p_username
#     ) THEN
#         UPDATE phonebook2
#         SET phone = p_phone
#         WHERE username = p_username;
#     ELSE
#         INSERT INTO phonebook2(username, phone)
#         VALUES (p_username, p_phone);
#     END IF;
# END;
# $$;


# 3. Процедура для вставки нескольких пользователей:
# ---------------------------------------------------
# CREATE OR REPLACE PROCEDURE insert_many_users(
#     IN user_names TEXT[],
#     IN user_phones TEXT[]
# )
# LANGUAGE plpgsql
# AS $$
# DECLARE
#     i INT;
#     current_name TEXT;
#     current_phone TEXT;
# BEGIN
#     FOR i IN 1..array_length(user_names, 1) LOOP
#         current_name := user_names[i];
#         current_phone := user_phones[i];
#
#         IF current_phone ~ '^[0-9]+$' THEN  -- Проверка: только цифры
#             INSERT INTO phonebook2(username, phone)
#             VALUES (current_name, current_phone)
#             ON CONFLICT (username) DO UPDATE
#             SET phone = EXCLUDED.phone;
#         END IF;
#     END LOOP;
# END;
# $$;
