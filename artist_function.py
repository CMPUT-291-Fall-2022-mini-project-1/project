import sqlite3

from typing import List
from ui_design.ui_artist import *
from sql_cmd.sql_artist import *
from user_song import Song


class ArtistMode():
    def __init__(self, aid, conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        self.aid = aid
        self.conn = conn
        self.cur = cursor

    def start_artist(self) -> None:
        artist_action = {
            "1": self.add_song,
            "2": self.find_top_fan_playlist,
            "3": self.end,
            "4": self.end
        }

        while True:
            print(UI_ARTIST_MAIN)
            action = input("Select an action to proceed: ")
            if action not in artist_action:
                print("Please make a proper selection.")
                continue

            # run that action
            artist_action[action]()

            if action == "3":
                return
            if action == "4":
                exit()

    def add_song(self) -> None:
        while True:
            title = input(
                "Please enter the title: ")
            titlecheck = set(title.split(" "))
            titlecheck.discard("")
            if (len(titlecheck) == 0):
                print("Please enter a valid title.")
                continue

            duration = input("Please enter the duration in seconds: ")
            try:
                duration = round(float(duration))
            except ValueError:
                print("Please enter a numeric duration")
                continue
            break

        self.cur.execute(SQL_ARTIST_CHECK_SONG_EXIST,
                         (self.aid, title, duration))
        res = self.cur.fetchall()

        if (len(res) > 0):
            print("This song already exists!")
        else:
            self.cur.execute(SQL_ARTIST_GET_NEW_SID)
            new_sid = self.cur.fetchall()
            sid = int(new_sid[0][0]) + 1

            self.cur.execute(SQL_ARTIST_INSERT_INTO_SONGS,
                             (sid, title, duration))
            self.conn.commit()
            self.cur.execute(SQL_ARTIST_INSERT_INTO_PERFORM,
                             (self.aid, sid))
            self.conn.commit()
            print("Insert successful")

    def find_top_fan_playlist(self) -> None:
        self.cur.execute(SQL_ARTIST_GET_TOP_USERS_PLAYLIST,
                         (self.aid, self.aid))
        results = self.cur.fetchall()
        find_top_users_playlists_display(
            ("Type", "Name"), results)
        # for i in users:
        #     print(i)

    def end(self) -> None:
        return
