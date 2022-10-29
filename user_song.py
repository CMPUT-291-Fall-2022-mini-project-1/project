import sqlite3
import sys
from sql_cmd.sql_song import *
from ui_design.ui_song import *

class Song():
    
    def __init__(self, sid:int, name:str, duration:int, user) -> None:
        self.sid = sid
        self.name = name
        self.duration = duration
        self.user = user
        user.cur.execute(SQL_SONG_ARTIST, (sid,))
        res = user.cur.fetchall()
        if len(res) == 0:
            self.artist = "can't find"
        else:
            self.artist = ""
            for artist in res:
                self.artist += artist[0]+", "
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
        self.user.cur.execute(SQL_CHECK_PLAYLIST, (self.user.uid,))
        user_playlists = {}
        user_action = {}
        cnt = 0
        for playlist in self.user.cur.fetchall():
            cnt += 1
            user_playlists[playlist[0]] = playlist[1]
            user_action[cnt] = playlist[0]
        action_str = ""
        for index, pid in user_action.items():
            action_str += "-{}. {}\n".format(str(index), user_playlists[pid])
        user_action[cnt+1] = -1
        user_action[cnt+2] = -1
        action_str += "-{}. In a new playlist\n".format(str(cnt+1))
        action_str += "-{}. <---".format(str(cnt+2))
        while True:
            print(UI_PLAYLISTS.format(action_str))
            try:
                selection = int(input("Select your playlist: "))
                if selection not in user_action.keys():
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Please select a valid option.")
                continue
        if selection == cnt+1:
            while True:
                title = input("Input new playlist title: ")
                if title is not None and len(title)!=0:
                    break
            self.user.cur.execute(SQL_MAX_PID)
            res = self.user.cur.fetchall()
            if res[0][0] is None:
                pid = 1
            else:
                pid = res[0][0]+1
            self.user.cur.execute(SQL_NEW_PLAYLIST, (pid, title, self.user.uid))
            self.user.conn.commit()
            self.user.cur.execute(SQL_ADD_PLAYLIST, (pid,self.sid, 1))
            self.user.conn.commit()
            self.playlists[pid] = title
        elif selection == cnt+2:
            return
        else:
            self.user.cur.execute(SQL_CHECK_PLINCLUDE, (user_action[selection], self.sid))
            if len(self.user.cur.fetchall()) != 0:
                print("already exists")
                self.user.conn.commit()
            else:
                self.user.cur.execute(SQL_ORDER, (user_action[selection],))
                res = self.user.cur.fetchall()
                if res[0][0] is None:
                    order = 1
                else:
                    order = res[0][0]+1
                self.user.cur.execute(SQL_ADD_PLAYLIST, (user_action[selection],self.sid, order))
                self.user.conn.commit()
                self.playlists[user_action[selection]] = user_playlists[user_action[selection]]
        return

    def passfun(self):
        return

    def select_song(self) -> None:
        user_action = {
            "1":self.listen,
            "2":self.info,
            "3":self.add_playlist,
            "4":self.passfun,
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
    from user_function import UserMode
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