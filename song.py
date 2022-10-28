import sqlite3
import sys
from sql_cmd.sql_song import *
from ui_design.ui_song import *
from user_function import UserMode

class Song():
    
    def __init__(self, sid:int, name:str, duration:int, user:UserMode) -> None:
        self.sid = sid
        self.name = name
        self.duration = duration
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
        if self.user.current_session is None:
            print("Auto start a session")
            self.user.start_session()
        self.user.cur.execute(SQL_CHECK_LISTEN, (self.sid, self.user.uid, self.user.current_session))
        if len(self.user.cur.fetchall()) == 0:
            self.user.cur.execute(SQL_LISTEN_NEW, (self.user.uid, self.user.current_session, self.sid))
            self.user.conn.commit()
        else:
            self.user.cur.execute(SQL_LISTEN_OLD, (self.user.uid, self.sid, self.user.current_session))
            self.user.conn.commit()
        return

    def info(self) -> None:
        playlists = ""
        for pid,title in self.playlists.items():
            playlists+="\n      {} : {}".format(pid,title)
        print(UI_INFO.format(self.name, str(self.sid), self.artist, str(self.duration), playlists))
        input("Press Enter to back...")
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
            print(UI_SONG_MAIN.format(self.name,self.name))
            action = input("Select an action to proceed: ")
            if action not in user_action:
                print("Please make a proper selection.")
                continue
            
            # run that action
            user_action[action]()
        
            if action == "4":
                return
            if action == "5":
                exit()
        return

connection:sqlite3.Connection = None
cursor:sqlite3.Cursor = None

def connect(path:str) -> None:
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def main(path: str) -> None:
    global connection, cursor
    connect(path)
    user_mode = UserMode("t1", connection, cursor)
    song = Song(10, "Nice for what", 210, user_mode)
    song.select_song()



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Database not specified!")
        exit()
    main(sys.argv[1])