import sqlite3

# from sql_cmd.sql_user import SQL_SONG_COUNT

UI_ARTIST_MAIN = """
-----------------Artist Screen-------------------
- 1. Add a song
- 2. Find top fans and playlists
- 3. Logout
- 4. Exit
-----------------Artist Screen-------------------
"""


def find_top_users_playlists_display(display_cols, i):
    i = i

    for c in display_cols:
        print("- %3d %10s %50s " % (i, c[0], c[1]))
        i += 1
    return i
