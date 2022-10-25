import getpass
import sqlite3
import sys




debug = True
connection:sqlite3.Connection = None
cursor:sqlite3.Cursor = None




def connect(path: str) -> None:
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def login_screen() -> None:
        while True:
            print("-----------------Login Screen-------------------\n")
            user_select = str(input("login/signup/exit\ndefault = exit\n")).lower()
            if user_select == 'login':
                login()
                pass
            elif user_select == 'signup':
                signup()
                pass
            else:
                exit()


def login() -> None:
    login_artist_sql_cmd = """
    SELECT aid, name, nationality
    FROM artists
    WHERE
    artists.aid = ?
    AND
    artists.pwd = ?
    """
    login_user_sql_cmd = """
    SELECT uid, name
    FROM users
    WHERE
    users.uid = ?
    AND
    users.pwd = ?
    """

    while True:
        id = input("input your aid/uid\n")
        passwd = getpass.getpass("input your password\n")
        if(id == None or passwd == None or len(id) == 0 or len(passwd) == 0):
            print("ERROR: id or password is empty\n")
            continue

        """
        try login as an artist
        """

        cursor.execute(login_artist_sql_cmd, (id, passwd))
        response_sql : list = cursor.fetchall()
        if len(response_sql) == 0:
            """
            fail login as an artist
            try login as a user
            """
            cursor.execute(login_user_sql_cmd, (id, passwd))
            response_sql : list = cursor.fetchall()
            if len(response_sql) == 0:
                # login fail
                print("can't login in, check the user/artists id and password\n")
                continue
            else:
                uid = response_sql[0][0]
                user_name = response_sql[0][1]
                print('login successful, {}\n'.format(user_name))
                user_system_functionalities(uid, user_name)
                break
        else:
            aid = response_sql[0][0]
            artist_name = response_sql[0][1]
            nationality = response_sql[0][2]
            print('login successful\n, {}'.format(artist_name))
            artist_system_functionalities(aid, artist_name, nationality)
            break


def signup():
    per_signup_sql_cmd = """
    SELECT *
    FROM users, artists
    WHERE users.uid = ?
    OR
    artists.aid = ?;
    """
    signup_sql_cmd = """
    INSERT INTO users VALUES (?, ?, ?);
    """

    
    uid = input('Provid a unique uid\n')
    user_name = input('Provid a name\n')
    passwd = getpass.getpass('Provid a password\n')
    if(uid == None or user_name == None or passwd == None or len(uid) == 0 or len(user_name) == 0 or len(passwd) == 0):
        print("ERROR: uid or name or password is empty\n")
        signup()
    cursor.execute(per_signup_sql_cmd, (uid, uid))
    if len(cursor.fetchall())!=0:
        print('uid mast be unique\n')
        signup()
    else:
        cursor.execute(signup_sql_cmd, (uid, user_name, passwd))
        connection.commit()
    pass

def user_system_functionalities(uid: str, user_name: str) -> None:
    print("-----------------User System Functionalities-------------------\n")
    #TODO
    pass

def artist_system_functionalities(aid: str, artist_name: str, nationality: str) -> None:
    print("-----------------Artist System Functionalities-------------------\n")
    #TODO
    pass


def main(path: str) -> None:
    global connection, cursor
    connect(path)
    login_screen()


if __name__ == "__main__":
    main(sys.argv[1])