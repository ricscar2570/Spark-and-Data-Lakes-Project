CREATE TABLE songplays (
    songplay_id BIGINT IDENTITY(0,1),
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR,
    PRIMARY KEY (songplay_id)
);
