import os
import codecs
from time import time
from datetime import datetime
import mysql.connector as mariadb


def main():
    start = time()

    # Connect with database
    mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
    cursor = mariadb_connection.cursor()

    # Delete table if exists
    cursor.execute("DROP TABLE IF EXISTS tracks;")

    # Create new tracks table
    create_tracks_table_sql = """
    CREATE TABLE tracks (
      id          INT NOT NULL AUTO_INCREMENT,
      song_id     VARCHAR(20) NOT NULL,
      artist      VARCHAR(500) DEFAULT NULL,
      title       text DEFAULT NULL,
      PRIMARY KEY (id)
    );
    """
    cursor.execute(create_tracks_table_sql)

    # Load data to tracks table
    path = f'{os.getcwd()}/unique_tracks_formatted.txt'
    cursor.execute("LOAD DATA INFILE %s INTO TABLE tracks FIELDS TERMINATED BY '|' (song_id, artist, title);", (path,))
    mariadb_connection.commit()
    mariadb_connection.close()

    # Load missing records (with | separator)
    with codecs.open('with_separator.txt', 'r', encoding='UTF-8') as data:
        records = []
        for line in data.read().split('\n')[:-1]:
            l_line = line.split("<SEP>", -1)
            records.append((l_line[1], l_line[2], l_line[3]))

        mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
        cursor = mariadb_connection.cursor()
        cursor.executemany("INSERT INTO tracks (song_id, artist, title) VALUES (%s, %s, %s)", records)
        mariadb_connection.commit()
        mariadb_connection.close()

    mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
    cursor = mariadb_connection.cursor()
    # Create indexes on tracks table
    cursor.execute("CREATE OR REPLACE INDEX tracks_song_id_index ON tracks (song_id);")
    cursor.execute("CREATE OR REPLACE INDEX tracks_artist_index ON tracks (artist);")

    # Delete table if exists
    cursor.execute("DROP TABLE IF EXISTS samples;")
    cursor.execute("DROP TABLE IF EXISTS dates;")

    # Create new dates table
    create_dates_table_sql = """
    CREATE TABLE dates (
      id          INT NOT NULL,
      year        SMALLINT NOT NULL,
      month       TINYINT NOT NULL,
      PRIMARY KEY (id)
    );
    """
    cursor.execute(create_dates_table_sql)

    # Generate dates records from 01.2000 to 12.2011
    date_records = []
    i = 1
    for year in range(2000, 2012):
        for month in range(1, 13):
            date_records.append((i, year, month))
            i += 1
    cursor.executemany("INSERT INTO dates (id, year, month) VALUES (%s, %s, %s)", date_records)

    # Create new samples table
    create_samples_table_sql = """
    CREATE TABLE samples (
      id                INT NOT NULL AUTO_INCREMENT,
      user_id           VARCHAR(100) NOT NULL,
      song_id           VARCHAR(20) NOT NULL,
      date_id           INT NOT NULL,
      PRIMARY KEY       (id)
    );
    """
    cursor.execute(create_samples_table_sql)
    mariadb_connection.commit()
    mariadb_connection.close()

    # Load data to samples table
    mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
    cursor = mariadb_connection.cursor()
    file_path = f'{os.getcwd()}/samples_formatted.txt'
    cursor.execute("LOAD DATA INFILE %s INTO TABLE samples FIELDS TERMINATED BY ' ' (user_id, song_id, date_id);", (file_path,))

    # Add indexes on samples
    cursor.execute("CREATE OR REPLACE INDEX samples_user_id_index ON samples (user_id);")
    cursor.execute("CREATE OR REPLACE INDEX samples_song_id_index ON samples (song_id);")
    cursor.execute("CREATE OR REPLACE INDEX samples_date_id_index ON samples (date_id);")

    mariadb_connection.commit()
    mariadb_connection.close()
    print('Execution time', time() - start)


if __name__ == "__main__":
    main()
