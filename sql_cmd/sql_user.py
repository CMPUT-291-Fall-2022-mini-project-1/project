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