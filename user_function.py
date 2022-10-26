import sqlite3

from typing import List
from ui_design.ui_user import *
from sql_cmd.sql_user import *


class UserMode():
    
    def __init__(self, uid, conn:sqlite3.Connection, cursor:sqlite3.Cursor) -> None:
        self.uid = uid
        self.current_session = None
        self.conn = conn
        self.cur = cursor

    def start_session(self) -> bool:
        
        self.cur.execute(SQL_USER_START_SESSION_GET_ALL_SESSIONS, (self.uid,))
        res = self.cur.fetchall()
        
        if len(res) == 0:
            self.current_session = 1
        else:
            self.current_session = res[0][0] + 1
        
        self.cur.execute(SQL_USER_START_SESSION_SUCCESS, (self.uid, self.current_session))
        self.conn.commit()
        
        return True


    def search_for_songs_playlists(self) -> None:
        # TODO
        pass


    def search_for_artists(self) -> None:
        # TODO
        pass


    def end_session(self) -> bool:
        
        if self.current_session is None:
            print("No session currently runs.")
            return False

        self.cur.execute(SQL_USER_END_SESSION_SUCCESS, (self.uid, self.current_session))
        self.conn.commit()
        self.current_session = None
        return True


    def start_user(self) -> None:
    
        print(UI_USER_MAIN)
        user_action = {
            "1": self.start_session,
            "2": self.search_for_songs_playlists,
            "3": self.search_for_artists,
            "4": self.end_session,
            "5": None
        }
        
        # select an action to proceed
        while True:
            action = input("Select an action to proceed: ")
            if action not in user_action:
                print("Please make a proper selection.")
                continue
        
            if action == "5":
                return
        
            # run that action
            user_action[action]()
        