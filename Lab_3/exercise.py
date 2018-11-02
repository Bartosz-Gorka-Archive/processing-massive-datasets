import codecs
import sqlite3
from time import time
from datetime import datetime


def create_tracks_table(conn):
    conn.execute('DROP TABLE IF EXISTS tracks')
    sql = '''
    CREATE TABLE tracks (
      song_id     TEXT PRIMARY KEY,
      artist      TEXT DEFAULT NULL,
      title       TEXT DEFAULT NULL
    )
    '''
    conn.execute(sql)


def tracks_data():
    data = codecs.open('unique_tracks.txt', 'r', encoding='iso-8859-2')
    records = []
    for line in data.read().split('\n')[:-1]:
        row = line.split('<SEP>', -1)
        try:
            records.append({
            'song_id': row[1],
            'artist': row[2],
            'title': row[3]
            })
        except Exception:
            records.append({
            'song_id': row[1],
            'artist': row[2],
            'title': ''
            })
    return records


def insert_into_tracks(conn, records):
    sql_command = "INSERT OR REPLACE INTO tracks (song_id, artist, title) VALUES (:song_id, :artist, :title)"
    conn.executemany(sql_command, records)


def create_indexes_tracks(conn):
    conn.execute('DROP INDEX IF EXISTS tracks_artist_index')
    conn.execute('CREATE INDEX tracks_artist_index ON tracks (artist)')


def create_dates_table(conn):
    conn.execute('DROP TABLE IF EXISTS dates')
    sql = '''
    CREATE TABLE dates (
      id     INTEGER PRIMARY KEY,
      year   INTEGER NOT NULL,
      month  INTEGER NOT NULL
    )
    '''
    conn.execute(sql)


def insert_into_dates(conn):
    records = []
    i = 1
    for year in range(2000, 2012):
        for month in range(1, 13):
            records.append({
            'id': i,
            'year': year,
            'month': month
            })
            i += 1

    sql_command = "INSERT OR REPLACE INTO dates (id, year, month) VALUES (:id, :year, :month)"
    conn.executemany(sql_command, records)


def build_structure(line):
    row = line.rstrip('\n').split('<SEP>')
    date = datetime.utcfromtimestamp(int(row[2]))

    return {
    'user_id': row[0],
    'song_id': row[1],
    'date_id': 12*(date.year - 2000) + date.month
    }


def samples_data():
    # data = open('test.txt', 'r')
    data = open('triplets_sample_20p.txt', 'r')
    return [build_structure(item) for item in data.readlines()]


def create_samples_table(conn):
    conn.execute('DROP TABLE IF EXISTS samples')
    sql = '''
    CREATE TABLE samples (
      ID                INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id           TEXT NOT NULL,
      song_id           TEXT NOT NULL,
      date_id           INTEGER NOT NULL
    )
    '''
    conn.execute(sql)


def insert_into_samples(conn, records):
    sql_command = "INSERT OR REPLACE INTO samples (user_id, song_id, date_id) VALUES (:user_id, :song_id, :date_id)"
    conn.executemany(sql_command, records)


def create_indexes_samples(conn):
    conn.execute('DROP INDEX IF EXISTS samples_song_id_index')
    conn.execute('CREATE INDEX samples_song_id_index ON samples (song_id)')


def show(row):
    print(' '.join([str(i) for i in row]))


def exercise_1(conn):
    sql = '''
    SELECT tracks.title, tracks.artist, sub.total_count
    FROM (
      SELECT
        song_id,
        COUNT(song_id) AS total_count
      FROM
        samples
      GROUP BY
        song_id
      ORDER BY
        total_count DESC
      LIMIT 10
    ) sub
    INNER JOIN tracks ON (tracks.song_id = sub.song_id)
    ORDER BY sub.total_count DESC;
    '''

    return conn.execute(sql)


def exercise_2(conn):
    sql = '''
    SELECT
      user_id,
      COUNT(DISTINCT song_id) AS counter
    FROM
      samples
    GROUP BY
      user_id
    ORDER BY
      counter DESC
    LIMIT 10;
    '''

    return conn.execute(sql)


def exercise_3(conn):
    sql = '''
    SELECT
      t.artist,
      COUNT(t.artist) AS counter
    FROM
      tracks AS t
    INNER JOIN samples AS l ON (l.song_id = t.song_id)
    GROUP BY
      t.artist
    ORDER BY
      counter DESC
    LIMIT 1;
    '''

    return conn.execute(sql)


def exercise_4(conn):
    sql = '''
    SELECT
      (((date_id + 11) % 12) + 1) AS date_month,
      COUNT(date_id)
    FROM
      samples
    GROUP BY
      date_month
    ORDER BY
      date_month ASC;
    '''

    return conn.execute(sql)


def exercise_5(conn):
    pass

def main():
    start = time()
    # Set connection with SQLite database
    conn = sqlite3.connect('pmd.db')

    # # Create tracks table
    create_tracks_table(conn)

    # Prepare and load data to table
    records = tracks_data()
    insert_into_tracks(conn, records)
    create_indexes_tracks(conn)

    # Create dates table
    create_dates_table(conn)

    # Load content to date's table
    insert_into_dates(conn)

    # Prepare and load samples
    records = samples_data()
    create_samples_table(conn)
    insert_into_samples(conn, records)
    create_indexes_samples(conn)

    # Exercise 1
    print('\nExercise 1')
    for row in exercise_1(conn):
        show(row)
    print(time() - start)

    # Exercise 2
    print('\nExercise 2')
    for row in exercise_2(conn):
        show(row)
    print(time() - start)

    # Exercise 3
    print('\nExercise 3')
    for row in exercise_3(conn):
        show(row)
    print(time() - start)

    # Exercise 4
    print('\nExercise 4')
    for row in exercise_4(conn):
        show(row)
    print(time() - start)

    # Exercise 5
    print('\nExercise 5')
    for row in exercise_5(conn):
        show(row)
    print(time() - start)

    conn.commit()
    conn.close()
    print(time() - start)


if __name__ == "__main__":
    main()
