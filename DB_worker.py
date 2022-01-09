import sqlite3

name_bd = 'user_data.db'


def create_db_and_table(arg_name_bd):
    with sqlite3.connect(arg_name_bd) as main_db:
        cursor = main_db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserData(
            UserID INT PRIMARY KEY,
            CityName VARCHAR(20) NULL,
            Busyness VARCHAR(20) NULL
        )
        """)


def save_data(arg_db_name, arg_user_id, arg_city_name=None, arg_busyness=None):
    with sqlite3.connect(arg_db_name) as arg_main_db:
        arg_cursor = arg_main_db.cursor()
        if arg_city_name is None and arg_busyness is None:
            arg_cursor.execute(f"""
                            INSERT INTO UserData
                    (UserID, CityName, Busyness)
                    VALUES ({arg_user_id}, NULL, NULL);
                """)
        else:
            arg_cursor.execute(f"""
                INSERT INTO UserData
                    (UserID, CityName, Busyness)
                    VALUES ({arg_user_id}, '{arg_city_name}', '{arg_busyness}');
                """)


def update_city_name(arg_db_name, arg_user_id, arg_city_name):
    with sqlite3.connect(arg_db_name) as arg_main_db:
        arg_cursor = arg_main_db.cursor()
        arg_cursor.execute(f"""
            UPDATE UserData
            SET CityName = '{arg_city_name}'
            WHERE UserID = {arg_user_id};
        """)


def update_busyness(arg_db_name, arg_user_id, arg_busyness):
    with sqlite3.connect(arg_db_name) as arg_main_db:
        arg_cursor = arg_main_db.cursor()
        arg_cursor.execute(f"""
            UPDATE UserData
            SET Busyness = '{arg_busyness}'
            WHERE UserID = {arg_user_id};
        """)


def delete_data(arg_db_name, arg_user_id=None):
    with sqlite3.connect(arg_db_name) as arg_main_db:
        arg_cursor = arg_main_db.cursor()
        queue = f"""
            DELETE FROM UserData
            """
        if arg_user_id is not None:
            queue += f"WHERE UserID = {arg_user_id}"
        arg_cursor.execute(queue)


def get_data(arg_db_name, arg_user_id=None):
    with sqlite3.connect(arg_db_name) as arg_main_db:
        arg_cursor = arg_main_db.cursor()
        queue = f"""
            SELECT UserID, CityName, Busyness FROM UserData
            """
        if arg_user_id is not None:
            queue += f"WHERE UserID = {arg_user_id}"
        arg_cursor.execute(queue)
        return arg_cursor.fetchall()


if __name__ == '__main__':
    delete_data(name_bd)
    save_data(name_bd, "1789")
    # update_data(name_bd, "1789", "Borispol", "Своя занятость")
    print(get_data(name_bd))

    # for temp in list(map(str, func())):
    #     await sen mes (temp)

    # while True:
    #     user_id = input("Type the user_id\n")
    #     if user_id.strip().lower() == 'quit':
    #         break
    #
    #     city_name = input("Type the city_name\n")
    #     if city_name.strip().lower() == 'quit':
    #         break
    #
    #     busyness = input("Type the busyness\n")
    #     if busyness.strip().lower() == 'quit':
    #         break
    #     save_data(name_bd, user_id)
    # for temp in get_data(name_bd, ):
    #     print(temp[0], temp[1], temp[2])
