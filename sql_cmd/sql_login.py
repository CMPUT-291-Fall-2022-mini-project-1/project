SQL_LOGIN_USER = """
SELECT uid
FROM users
WHERE users.uid = ?
AND users.pwd = ?
"""

SQL_LOGIN_ARTIST = """
SELECT aid
FROM artists
WHERE artists.aid = ?
AND artists.pwd = ?
"""

SQL_SIGNUP_USER_CHECK = """
SELECT users.uid
FROM users
WHERE users.uid = ?

UNION

SELECT artists.aid
FROM artists
WHERE artists.aid = ?;
"""

SQL_SIGNUP_USER_SUCCESS = """
INSERT INTO users VALUES (?, ?, ?);
"""
