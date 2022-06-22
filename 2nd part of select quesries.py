import sqlalchemy

user = 'postgres'
password = #не хранить пароли в коде, не хранить пароли в коде
db = f'postgresql://{user}:{password}@localhost:5432/homework'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


def get_artists_in_genre() -> list:
    artist_in_each_genre = connection.execute("""
    SELECT genre_name, count(ag.artist_id) FROM genres g
    JOIN artistgenre ag ON ag.genre_id = g.genre_id 
    GROUP BY g.genre_name""").fetchall()
    return artist_in_each_genre


def get_tracks_in_albums_in_years(from_year: int, to_year: int) -> list:  # добавить данные в таблицу
    desired_tracks = connection.execute(f"""
    SELECT track_name FROM tracks t
    JOIN albums a ON t.album = a.album_id
    WHERE a.release_year BETWEEN {from_year} AND {to_year}""").fetchall()
    return desired_tracks


def get_avg_track_length_by_album() -> list:
    avg_length = connection.execute("""
    SELECT a.album_name, avg(track_length) FROM tracks t
    JOIN albums a ON t.album = a.album_id
    GROUP BY a.album_name""").fetchall()
    return avg_length


def get_relesed_except_year(exception_year: int) -> list:
    desired_artists = connection.execute(f"""
    SELECT artist_name FROM artists a
    JOIN artistalbum aa ON a.artist_id = aa.artist_id
    JOIN albums al ON aa.album_id = al.album_id
    WHERE NOT {exception_year} = al.release_year""").fetchall()
    return desired_artists


def get_mixtapes_containing_artist(artist_name: str) -> list:
    desired_mixtapes = connection.execute((f"""
    SELECT mixtape_name FROM mixtapes m
    JOIN tracksmixtapes tm ON m.mixtape_id = tm.mixtape_id
    JOIN tracks t ON tm.track_id = t.track_id
    JOIN albums al ON t.album = al.album_id
    JOIN artistalbum aa ON al.album_id = aa.album_id
    JOIN artists a ON aa.artist_id = a.artist_id
    WHERE '{artist_name}' = a.artist_name
    """)).fetchall()
    return desired_mixtapes


def get_albums_with_many_genres(num_of_genres: int = 1) -> list:
    desired_albums = connection.execute(f"""
    SELECT album_name FROM albums a
    JOIN artistalbum aa ON a.album_id = aa.album_id
    JOIN artists ar ON aa.artist_id = ar.artist_id
    JOIN artistgenre ag ON ar.artist_id = ag.artist_id
    WHERE (SELECT COUNT(artist_id) FROM artistgenre) > {num_of_genres}""").fetchall()
    return desired_albums


def not_in_mixtapes() -> list:
    desired_tracks = connection.execute("""
    SELECT track_name FROM tracks t
    LEFT JOIN tracksmixtapes tm ON tm.track_id = t.track_id
    WHERE tm.track_id IS NULL 
    """).fetchall()
    return desired_tracks


def artists_with_shortest_track() -> list:
    desired_artists = connection.execute("""
    SELECT artist_name FROM artists a
    JOIN artistalbum aa ON a.artist_id = aa.artist_id
    JOIN albums al ON aa.album_id = al.album_id
    JOIN tracks t ON al.album_id = t.album
    WHERE t.track_length = (SELECT MIN(track_length) FROM tracks)""").fetchall()
    return desired_artists


def least_tracks_in_album() -> list:
    desired_albums = connection.execute("""
    SELECT album_name FROM albums al
    JOIN tracks t ON t.album = al.album_id
    WHERE (SELECT COUNT(t.album)) = (SELECT MIN(COUNT(t.album)))""").fetchall()
    return desired_albums


print(get_tracks_in_albums_in_years(2019, 2020))
print(get_artists_in_genre())
print(get_avg_track_length_by_album())
print(get_relesed_except_year(2020))
print(get_mixtapes_containing_artist('A Day to Remember'))
print(get_albums_with_many_genres())
print(not_in_mixtapes())
print(artists_with_shortest_track())
