import sqlalchemy

user = 'postgres'
password = # не храните пароли в коде
db = f'postgresql://{user}:{password}@localhost:5432/homework'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()
random_artist_list = [
'Green Day', 'A Day to Remember', 'Architects', 'Four Year Strong',  
'Wage War', 'Obey the Brave', 'Knocked Loose', 'Terror'
    ]
random_genres = ['easycore', 'beatdown', 'hardcore', 'posthardcore', 'pop-punk']
random_albums = {
    'Gone Are The Good Days': 2021,
    'Manic': 2021,
    'Bad Vibrations': 2016, 
    'Mad Season': 2017,
    'Live By The Code': 2013,
    'Lost Forever // Lost Together': 2014, 
    'Laugh Tracks': 2016, 
    'American Idiot': 2004,
}
random_mixtapes = {
    2015: 'Awesome Mixtape',
    2016: 'Almost Awesome Mixtape',
    2017: 'Very Cool Mixtape',
    2018: 'Cool Mixtape',
    2019: 'Not So Cool Mixtape',
    2020: 'Totally Not Cool Mixtape',
    2021: 'Bad mixtape',
    2022: 'Would never listen to this mixtape'
}
random_tracks = [
    {
        'length': 222,
        'name': 'Gone Are The Good Days',
        'album': 'Gone Are The Good Days'
    },
    {
        'length': 164,
        'name': 'Manic',
        'album': 'Manic'
    },
    {   'length': 212,
        'name': 'Never Gonna Give You Up',
        'album': 'American Idiot'
         # time for rickroll
    },
    {
        'length': 213,
        'name': 'Bad Vibrations',
        'album': 'Bad Vibrations'
    },
    {
        'length': 221,
        'name': '97 Again',
        'album': 'Mad Season'
    },
    {
        'length': 163,
        'name': 'Hard Lessons',
        'album': 'Live By The Code'
    },
    {
        'length': 245,
        'name': 'Gravedigger',
        'album': 'Lost Forever // Lost Together'
    },
    {
        'length': 134,
        'name': 'Billy No Mates',
        'album': 'Laugh Tracks'
    },
    {
        'length': 174,
        'name': 'American Idiot',
        'album': 'American Idiot'
    },
    {
        'length': 250,
        'name': 'I',
        'album': 'Mad Season'
    },
    {
        'length': 260,
        'name': 'Dont Know',
        'album': 'Laugh Tracks'
    },
    {
        'length': 270,
        'name': 'What',
        'album': 'Live By The Code'
    },
    {
        'length': 280,
        'name': 'To',
        'album': 'Bad Vibrations'
    },
    {
        'length': 290,
        'name': 'Add',
        'album': 'Lost Forever // Lost Together'
    },
    {
        'length': 300,
        'name': 'To this',
        'album': 'American Idiot'
    }
]
artist_genre_combo = {
    'Green Day': 'pop-punk',
    'A Day to Remember': 'easycore',
    'Architects': 'posthardcore',
    'Four Year Strong': 'easycore',
    'Wage War': 'posthardcore',
    'Obey the Brave': 'beatdown',
    'Knocked Loose': 'beatdown',
    'Terror': 'hardcore'
}
artist_album = {
    'Green Day': 'American Idiot',
    'A Day to Remember': 'Bad Vibrations',
    'Architects': 'Lost Forever // Lost Together',
    'Four Year Strong': 'Gone Are The Good Days', # на самом деле нет, но я не думаю, что это важно
    'Wage War': 'Manic',
    'Knocked Loose': 'Laugh Tracks',
    'Terror': 'Live By The Code'
}
tracks_mixtapes = {
    'Never Gonna Give You Up': 'Awesome Mixtape',
    'Gone Are The Good Days': 'Almost Awesome Mixtape',
    'Gravedigger': 'Very Cool Mixtape',
    'Bad Vibrations': 'Cool Mixtape',
    'I': 'Not So Cool Mixtape',
    'Dont Know': 'Totally Not Cool Mixtape',
    'What': 'Bad mixtape',
    'To': 'Would never listen to this mixtape'
}
def add_artists(artists: list) -> None:
    for artist in artists:
        connection.execute(f"""
        INSERT INTO artists(artist_name)
            VALUES('{artist}')
        ON CONFLICT DO NOTHING;""")

def add_genres(genres: list) -> None:
    for genre in genres:
        connection.execute(f"""
        INSERT INTO genres(genre_name)
            VALUES('{genre}')
        ON CONFLICT DO NOTHING""")

def add_albums(albums: dict) -> None:
    for album, year in albums.items():
        connection.execute(f"""
        INSERT INTO albums(release_year, album_name)
            VALUES ({year}, '{album}')
        ON CONFLICT DO NOTHING;""")

def add_mixtapes(mixtapes: dict) -> None:
    for year, mixtape in mixtapes.items():
        connection.execute(f"""
        INSERT INTO mixtapes(release_year, mixtape_name)
            VALUES ({year}, '{mixtape}')
        ON CONFLICT DO NOTHING;""")

def add_tracks(tracks: list) -> None:
    for track in tracks:
        connection.execute(f"""
        INSERT INTO tracks(track_length, track_name, album)
            VALUES ({track['length']}, '{track['name']}', 
            (SELECT album_id FROM albums WHERE album_name = '{track['album']}'))
        ON CONFLICT DO NOTHING;""")

def artist_genres_combining(artist_genres_pairs: dict) -> None:
    for artist, genre in artist_genres_pairs.items():
        connection.execute(f"""
        INSERT INTO artistgenre(artist_id, genre_id)
            VALUES((SELECT artist_id FROM artists WHERE artist_name = '{artist}'),
            (SELECT genre_id FROM genres WHERE genre_name = '{genre}'))
        ON CONFLICT DO NOTHING;""")

def artist_album_combining(artist_album_pairs: dict) -> None:
    for artist, album in artist_album_pairs.items():
        connection.execute(f"""
        INSERT into artistalbum(album_id, artist_id)
            VALUES ((SELECT album_id FROM albums WHERE album_name = '{album}'), 
            (SELECT artist_id FROM artists WHERE artist_name = '{artist}'))
        ON CONFLICT DO NOTHING;""")

def tracks_mixtapes_combining(track_mixtapes_pairs: dict) -> None:
    for track, mixtape in track_mixtapes_pairs.items():
        connection.execute(f"""
        INSERT into tracksmixtapes(track_id, mixtape_id)
            VALUES ((SELECT track_id FROM tracks WHERE track_name = '{track}'),
            (SELECT mixtape_id FROM mixtapes WHERE mixtape_name = '{mixtape}'))
        ON CONFLICT DO NOTHING;""")

    
add_artists(random_artist_list)
add_genres(random_genres)
add_albums(random_albums)
add_mixtapes(random_mixtapes)
add_tracks(random_tracks)
artist_genres_combining(artist_genre_combo)
artist_album_combining(artist_album)
tracks_mixtapes_combining(tracks_mixtapes)
print('Done')
