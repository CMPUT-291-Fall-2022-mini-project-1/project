from typing import List
from ui_design.ui_user import *


class UserMode():
    
    def __init__(self, conn, cursor) -> None:
        self.current_session = None
        self.conn = conn
        self.cur = cursor

    def start_session(self, sno:int) -> bool:
        pass


    def search_for_songs_playlists(self, keywords:List) -> None:
        pass


    def search_for_artists(self, keywords:List) -> None:
        pass


    def end_session(self) -> bool:
        pass


    def user_system_functionalities(self, uid:str) -> None:
    
        print(UI_USER_MAIN)
        user_action = {
            1: self.start_session,
            2: self.search_for_songs_playlists,
            3: self.search_for_artists,
            4: self.end_session
        }