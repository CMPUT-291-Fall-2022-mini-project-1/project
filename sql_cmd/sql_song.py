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

SQL_CHECK_LISTEN = """
SELECT listen.cnt
FROM listen
WHERE listen.sid = ?
AND listen.uid = ?
AND listen.sno = ?;
"""

SQL_LISTEN_NEW = """
insert into listen values (?, ?, ?, 1);
"""

SQL_LISTEN_OLD = """
UPDATE listen
SET cnt = cnt+1
WHERE listen.uid = ?
AND listen.sid = ?
AND listen.sno = ?;
"""