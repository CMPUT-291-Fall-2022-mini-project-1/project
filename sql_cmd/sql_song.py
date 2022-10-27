SQL_SONG_ARTIST = """
SELECT artists.name
FROM artists, perform
WHERE artists.aid = perform.aid
AND perform.sid = ?;
"""

SQL_PLAY_LISTS = """
SELECT playlists.pid, playlists.title
FROM plinclude, playlists
WHERE plinclude.sid = ?
AND playlists.pid = plinclude.pid;
"""