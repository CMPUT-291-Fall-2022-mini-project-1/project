SQL_LOGIN_USER = """
SELECT uid
FROM users
WHERE lower(users.uid) = lower(?)
AND users.pwd = ?
"""

SQL_LOGIN_ARTIST = """
SELECT aid
FROM artists
WHERE lower(artists.aid) = lower(?)
AND artists.pwd = ?
"""

SQL_SIGNUP_USER_CHECK = """
SELECT users.uid
FROM users
WHERE lower(users.uid) = lower(?)
"""

SQL_SIGNUP_USER_SUCCESS = """
INSERT INTO users VALUES (?, ?, ?);
"""
