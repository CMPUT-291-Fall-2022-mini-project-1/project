import sqlite3

from sql_cmd.sql_user import SQL_SONG_COUNT

UI_USER_MAIN = """
-----------------User Screen-------------------
- 1. Start a session
- 2. Search for songs & playlists
- 3. Search for artists
- 4. End the session
- 5. Logout
- 6. Exit
-----------------User Screen-------------------
"""

def search_artists_display(titles, display_cols, cur:sqlite3.Cursor):
    print("-----------------Search Result--------------------")
    print("-     %20s %20s %15s" % titles)
    i = 1
    
    select_dict = {}
    final_select = None
    
    for c in display_cols:
        while i > 5:
            selection = input("Choose an artist or press ENTER to see more: ")
            if selection == "":
                i = 1
                select_dict = {}
            elif selection not in select_dict:
                print("Invalid selection.")
            else:
                i = 1
                final_select = select_dict[selection]
                break
        
        if final_select is not None:
            break
        
        # get the number of performed songs
        cur.execute(SQL_SONG_COUNT, (c[0],))
        res = cur.fetchall()[0][0]
        
        print("- %3d %20s %20s %15d" % (i, c[1], c[2], res))
        select_dict[str(i)] = c
        i += 1
    
    print("--------------End of Search Result----------------")
    while final_select is None:
        if len(select_dict) == 0:
            return None
        
        selection = input("Choose an artist or press ENTER to cancel: ")
        if selection == "":
            return None
        elif selection not in select_dict:
            print("Invalid selection.")
        else:
            return select_dict[selection]
    
    return final_select


def search_songs_playlists_display(titles, display_cols):
    print("-----------------Search Result--------------------")
    print("-     %10s %10s %50s %10s" % titles)
    i = 1
    
    select_dict = {}
    final_select = None
    
    for c in display_cols:
        while i > 5:
            selection = input("Choose a song/playlist or press ENTER to see more: ")
            if selection == "":
                i = 1
                select_dict = {}
            elif selection not in select_dict:
                print("Invalid selection.")
            else:
                i = 1
                final_select = select_dict[selection]
                break
        
        if final_select is not None:
            break
            
        print("- %3d %10s %10d %50s %10d" % (i, c[0], c[1], c[2], c[3]))
        select_dict[str(i)] = c
        i += 1

    print("--------------End of Search Result----------------")
    while final_select is None:
        if len(select_dict) == 0:
            return None
        
        selection = input("Choose a song/playlist or press ENTER to cancel: ")
        if selection == "":
            return None
        elif selection not in select_dict:
            print("Invalid selection.")
        else:
            return select_dict[selection]
    
    return final_select
