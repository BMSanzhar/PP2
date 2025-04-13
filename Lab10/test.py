# import psycopg2
# from tabulate import tabulate


# conn=psycopg2.connect(
#     host="localhost",
#     dbname="phonebook_db",
#     user="postgres",
#     password="87277478111",
#     port="5432"
# )

# cur=conn.cursor()

# username=input("Please enter the username: ")
# number=input("Number: ")


# cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, number))
# conn.commit()

# cur.execute("SELECT * FROM phonebook")
# rows=cur.fetchall()

# headers = ["ID", "Username", "Phone"]

# print(tabulate(rows, headers=headers, tablefmt="pretty"))

# print("Данные добавлены")

# cur.close()
# conn.close()


import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    dbname="snake_db",
    user="postgres",
    password="87277478111",
    port="5432"
)

cur = conn.cursor()
cur.execute("DELETE FROM user_score")
# Пример вставки данных вручную


conn.commit()

# Закрываем соединение
cur.close()
conn.close()
