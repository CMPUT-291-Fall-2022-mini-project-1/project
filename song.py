import re
import sqlite3
from unicodedata import name
from sql_cmd.sql_song import *
from ui_design.ui_song import *
from user_function import UserMode

class Song():
    
    def __init__(self, sid:int, name:str, duration:int, user:UserMode) -> None:
        self.sid = sid
        self.name = name
        self.duration = duration
        self.conn:sqlite3.Connection = user.conn
        self.cursor:sqlite3.Cursor = user.cur
        self.user = user
        user.cur.execute(SQL_SONG_ARTIST, (sid,))
        res = user.cur.fetchall()
        if len(res) == 0:
            self.artist = "can't find"
        else:
            self.artist = res[0][0]
        play_lists_tmp = {}
        user.cur.execute(SQL_PLAY_LISTS, (sid,))
        for playlist in user.cur.fetchall():
            play_lists_tmp[playlist[0]] = playlist[1]
        self.playlists = play_lists_tmp
        return
    
    def listen(self) -> None:
        #TODO
        pass
        return

    def info(self) -> None:
        #TODO
        pass
        return

    def add_playlist(self) -> None:
        #TODO
        pass
        return

    def select_song(self) -> None:
        user_action = {
            "1":self.listen,
            "2":self.info,
            "3":self.add_playlist,
            "4":self.user.end_session,
            "5":self.user.end_session,
        }


        while True:
            print(UI_SONG_MAIN.format(name,name))
        return




def test():
    pass



if __name__ == "main":
    test()