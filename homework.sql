create table if not exists genres(
    genre_id serial primary key,
    genre_name varchar(40) unique
);
create table if not exists artists(
    artist_id serial primary key,
    artist_name varchar(80) unique
);
create table if not exists artistgenre(
    artist_id integer references artists(artist_id),
    genre_id integer references genres(genre_id),
    constraint pk primary key (artist_id, genre_id)
);
create table if not exists albums(
    album_id serial primary key,
    album_name varchar(80) not null,
    release_year integer not null
);
create table if not exists artistalbum(
    artist_id integer references artists(artist_id),
    album_id integer references albums(album_id),
    constraint pk2 primary key (artist_id, album_id)
);
create table if not exists tracks(
    track_id serial primary key,
    track_length integer not null,
    track_name varchar(80) not null,
    album integer references albums(album_id)
);
create table if not exists mixtapes(
    mixtape_id serial primary key,
    mixtape_name varchar(80) not null,
    release_year integer not null
);
create table if not exists tracksmixtapes(
    id serial primary key,
    track_id integer references tracks(track_id),
    mixtape_id integer references mixtapes(mixtape_id)
);