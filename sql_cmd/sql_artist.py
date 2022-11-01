SQL_ARTIST_CHECK_SONG_EXIST = """
select title
from songs, perform
where songs.sid = perform.sid and perform.aid = ? and lower(title) = lower(?) and duration = ?;
"""

SQL_ARTIST_GET_NEW_SID = """
select max(sid)
from songs;
"""

SQL_ARTIST_INSERT_INTO_SONGS = """
insert into songs
values (?, ?, ?);
"""

SQL_ARTIST_INSERT_INTO_PERFORM = """
insert into perform
values (?, ?);
"""

SQL_ARTIST_GET_TOP_USERS_PLAYLIST = """
with top_users as(
    select "user" type, users.name name
    from users, perform, listen, songs
    where users.uid = listen.uid and perform.sid = listen.sid and songs.sid = listen.sid and perform.aid = ?
    group by users.uid
    order by sum(listen.cnt*songs.duration) desc
    limit 3
),

top_playlists as(
    select "playlists" type, playlists.title name
    from playlists, plinclude, perform
    where playlists.pid = plinclude.pid and plinclude.sid = perform.sid and perform.aid = ?
    group by playlists.pid
    order by count(plinclude.sid) desc
    limit 3
)

select * from top_users
union
select * from top_playlists
order by type desc;
"""
