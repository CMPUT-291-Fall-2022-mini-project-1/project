import getpass
import sqlite3
import sys

from sql_cmd.sql_login import *
from ui_design.ui_login import *

from user_function import UserMode
from artist_function import ArtistMode

debug = True
connection: sqlite3.Connection = None
cursor: sqlite3.Cursor = None


def connect(path: str) -> None:
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def login_screen() -> None:

    login_action = {
        1: login,
        2: sign_up,
        3: exit
    }

    while True:
        print(UI_LOGIN_MAIN)
        try:
            user_select = int(input("Enter your selection: "))
            if user_select not in login_action:
                raise ValueError
        except ValueError:
            print("Invalid selection!")
            continue
        if user_select <= 3 and user_select > 0:
            login_action[user_select]()
        else:
            print("can't conform your action, try again")
            continue


def login() -> None:
    global connection, cursor

    all_login_modes = {
        0: user_system_functionalities,
        1: artist_system_functionalities
    }

    while True:
        # get the id and password
        id, pwd = "", ""
        while id is None or len(id) == 0:
            id = input("User ID: ")
        while pwd is None or len(pwd) == 0:
            pwd = getpass.getpass("Password: ")

        # check validity
        valid_user, valid_artist = False, False

        cursor.execute(SQL_LOGIN_USER, (id, pwd))
        res_user = cursor.fetchall()
        valid_user = len(res_user) != 0

        cursor.execute(SQL_LOGIN_ARTIST, (id, pwd))
        res_artist = cursor.fetchall()
        valid_artist = len(res_artist) != 0

        # decide the login mode
        if not valid_user and not valid_artist:
            print("Invalid ID or password. Please try again.")
            continue
        if valid_user and valid_artist:
            while True:
                try:
                    login_mode = int(
                        input("Select your login mode (0.user, 1.artist): "))
                    if login_mode not in all_login_modes:
                        raise ValueError
                    else:
                        if login_mode == 0:
                            id = res_user[0][0]
                        else:
                            id = res_artist[0][0]
                        break
                except ValueError:
                    print("Please select a valid option.")
                    continue
        elif valid_user:
            id = res_user[0][0]
            login_mode = 0
        elif valid_artist:
            id = res_artist[0][0]
            login_mode = 1
        else:
            continue
        break

    all_login_modes[login_mode](id)


def sign_up():
    global connection, cursor

    # get all user info; make sure uid is unique
    while True:
        new_uid = input("Enter your user id: ")
        cursor.execute(SQL_SIGNUP_USER_CHECK, (new_uid,))
        if len(cursor.fetchall()) == 0:
            break
        else:
            print(
                "A user has used {} as his/her user id. Please choose another user id.".format(new_uid))
    new_name = input("Enter your user name: ")
    new_pwd = getpass.getpass("Enter your new password: ")

    # add new user to the database and start user system
    cursor.execute(SQL_SIGNUP_USER_SUCCESS, (new_uid, new_name, new_pwd))
    connection.commit()
    user_system_functionalities(new_uid)


def user_system_functionalities(uid: str) -> None:
    global connection, cursor
    user_mode = UserMode(uid, connection, cursor)
    user_mode.start_user()


def artist_system_functionalities(aid: str) -> None:
    global connection, cursor
    user_mode = ArtistMode(aid, connection, cursor)
    user_mode.start_artist()


def main(path: str) -> None:
    global connection, cursor
    connect(path)
    print(UI_WELCOME)
    login_screen()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Database not specified!")
        exit()
    main(sys.argv[1])
