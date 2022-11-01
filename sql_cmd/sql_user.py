SQL_USER_START_SESSION_GET_ALL_SESSIONS = """
select max(sno)
from sessions
where lower(uid) = lower(?);
"""

SQL_USER_START_SESSION_SUCCESS = """
insert into sessions
values (?, ?, date('now'), null);
"""

SQL_USER_END_SESSION_SUCCESS = """
update sessions
set end = date('now')
where lower(uid) = lower(?)
and sno = ?;
"""

SQL_USER_EXPAND_PLAYLIST = """
select songs.sid, songs.title, songs.duration
from songs, plinclude
where songs.sid = plinclude.sid
and plinclude.pid = ?;
"""

SQL_USER_EXPAND_ARTIST = """
select songs.sid, songs.title, songs.duration
from songs, perform
where songs.sid = perform.sid
and perform.aid = ?;
"""


SQL_ARTIST_INFO = """
with asinfo as (
    select artists.aid, songs.title stitle, artists.name, artists.nationality
    from artists, perform, songs
    where artists.aid = perform.aid
    and perform.sid = songs.sid
), 
"""

SQL_SONG_COUNT = """
select count(sid)
from perform
where aid = ?;
"""


def get_sql_search_artists(keywords: list):
    # get artists matching
    sql_str = SQL_ARTIST_INFO+"artist_search_collection as ("
    first = True

    input_list = []
    kw_id = 0
    for k in keywords:
        if not first:
            sql_str += " union "
        first = False
        sql_str += """
        select distinct asinfo.aid, asinfo.name, asinfo.nationality, {} kcount
        from asinfo
        where lower(asinfo.name) like ?
        or lower(asinfo.stitle) like ?
        """.format(kw_id)
        input_list.extend(["%"+k+"%"]*2)
        kw_id += 1

    sql_str += ")"
    sql_str += """
    select aid, name, nationality, count(kcount)
    from artist_search_collection
    group by aid, name, nationality
    order by count(kcount) desc;
    """
    return sql_str, tuple(input_list)


def get_sql_search_songs_playlists(keywords: list):
    # get songs matching
    sql_str = "with song_search_collection as ("
    first = True

    input_list = []
    kw_id = 0
    for k in keywords:
        if not first:
            sql_str += " union all "
        first = False
        sql_str += """
        select "song" type, sid id, title, duration, {} kcount
        from songs
        where lower(title) like ?
        """.format(kw_id)
        input_list.append("%"+k+"%")
        kw_id += 1

    # get duration for each pid
    sql_str += "), "
    sql_str += """
    playlist_duration as (
        select playlists.pid, playlists.title, sum(songs.duration) duration
        from playlists, plinclude, songs
        where playlists.pid = plinclude.pid
        and plinclude.sid = songs.sid
        group by plinclude.pid
        
        union
        
        select playlists.pid, playlists.title, 0 duration
        from playlists
        where playlists.pid not in (
            select pid
            from plinclude
        )
    ), 
    """

    # get playlist matching
    sql_str += "playlist_search_collection as ("
    first = True

    kw_id = 0
    for k in keywords:
        if not first:
            sql_str += " union all "
        first = False
        sql_str += """
        select "playlist" type, pid id, title, duration, {} kcount
        from playlist_duration
        where lower(title) like ?
        """.format(kw_id)
        input_list.append("%"+k+"%")
        kw_id += 1

    # union the two & order by keyword count
    sql_str += "), total_search_collection as ("
    sql_str += """
    select type, id, title, duration, kcount
    from song_search_collection
    union
    select type, id, title, duration, kcount
    from playlist_search_collection
    )
    """

    sql_str += """
    select type, id, title, duration, count(kcount)
    from total_search_collection
    group by type, id, title, duration
    order by count(kcount) desc;
    """

    return sql_str, tuple(input_list)
