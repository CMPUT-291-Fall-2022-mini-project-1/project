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

SQL_CHECK_PLAYLIST = """
SELECT playlists.pid, playlists.title
FROM playlists
WHERE playlists.uid = ?;
"""

SQL_ORDER = """
SELECT max(plinclude.sorder)
FROM plinclude
WHERE plinclude.pid = ?;
"""

SQL_ADD_PLAYLIST = """
INSERT INTO plinclude VALUES (?,?,?);
"""

SQL_NEW_PLAYLIST = """
INSERT INTO playlists VALUES (?,?,?)
"""

SQL_MAX_PID = """
SELECT max(playlists.pid)
FROM playlists;
"""

SQL_CHECK_PLINCLUDE = """
SELECT *
FROM plinclude
WHERE plinclude.pid = ?
AND
plinclude.sid = ?
"""