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

def get_sql_search_songs_playlists(keywords:list):
    # get songs first
    sql_str = "with song_search_collection as ("
    first = True
    
    input_list = []
    kw_id = 0
    for k in keywords:
        if not first:
            sql_str += " union all "
        first = False
        sql_str += """
        select "song", sid, title, duration, {}
        from songs
        where lower(title) like ?
        """.format(kw_id)
        input_list.append("%"+k+"%")
        kw_id += 1
    
    sql_str += ") select * from song_search_collection;"
    
    return sql_str, tuple(input_list)
