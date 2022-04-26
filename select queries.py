import sqlalchemy

user = 'postgres'
password = #не храните пароли в коде
db = f'postgresql://{user}:{password}@localhost:5432/homework'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

def name_year_of_album(year: int):
    x = connection.execute(f"""
    SELECT album_name, release_year FROM albums WHERE release_year = {year};""").fetchall()
    return x

def longest_track():
    x = connection.execute(f"""
    SELECT track_name, track_length FROM tracks ORDER by track_length DESC LIMIT 1;""").fetchone()
    return x

def longer_than_seconds(length: int):
    x = connection.execute(f"""
    SELECT track_name FROM tracks WHERE track_length > {length};""").fetchall()
    return x

def published_between(start: int, end: int):
    x = connection.execute(f"""
    SELECT mixtape_name FROM mixtapes WHERE release_year BETWEEN {start} AND {end};""").fetchall()
    return x

def one_word_bandname():
    x = connection.execute(f"""
    SELECT artist_name FROM artists WHERE artist_name NOT LIKE '%% %%';""").fetchall()
    return x

def track_contains(keyword: str):
    x = connection.execute(f"""
    SELECT track_name FROM tracks WHERE track_name LIKE '%%{keyword}%%';""").fetchall()
    return x

print(name_year_of_album(2018))
print(longest_track())
print(longer_than_seconds(210))
print(published_between(2018, 2020))
print(one_word_bandname())
print(track_contains('my'))
print(track_contains('мой'))
