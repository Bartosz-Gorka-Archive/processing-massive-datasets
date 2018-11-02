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
      track_id    VARCHAR(50) NOT NULL,
      song_id     VARCHAR(20) NOT NULL,
      artist      VARCHAR(500) DEFAULT NULL,
      title       text DEFAULT NULL,
      PRIMARY KEY (id)
    );
    """
    cursor.execute(create_tracks_table_sql)

    # Load data to tracks table
    path = f'{os.getcwd()}/unique_tracks_serialized.txt'
    cursor.execute("LOAD DATA INFILE %s INTO TABLE tracks FIELDS TERMINATED BY '<SEP>' (track_id, song_id, artist, title);", (path,))

    # Create indexes on tracks table
    cursor.execute("CREATE OR REPLACE INDEX tracks_song_id_index ON tracks (song_id);")
    cursor.execute("CREATE OR REPLACE INDEX tracks_artist_index ON tracks (artist);")

    # Delete table if exists
    cursor.execute("DROP TABLE IF EXISTS samples;")
    cursor.execute("DROP TABLE IF EXISTS dates;")

    # Commit changes and refresh connection with database
    mariadb_connection.commit()
    mariadb_connection.close()
    mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
    cursor = mariadb_connection.cursor()

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
      date_val          INT NOT NULL,
      date_id           INT NOT NULL,
      PRIMARY KEY       (id)
    );
    """
    cursor.execute(create_samples_table_sql)
    mariadb_connection.commit()
    mariadb_connection.close()

    # Make content in this large file
    # with open('triplets_sample_20p.txt', 'r') as sourcefile:
    #     content = sourcefile.readlines()
    #     with open('samples_formatted.txt', 'w') as textfile:
    #         for line in content:
    #             ll = line.replace('\n', '').split('<SEP>')
    #             year_month = [int(i) for i in datetime.utcfromtimestamp(int(ll[2])).strftime('%Y %m').split(' ')]
    #             textfile.writelines((ll[0], ' ', ll[1], ' ', str(12*(year_month[0] - 2000) + year_month[1]), '\n'))

    # Load data to samples table
    mariadb_connection = mariadb.connect(user='root', password='', database='pmd')
    cursor = mariadb_connection.cursor()
    file_path = f'{os.getcwd()}/samples_formatted.txt'
    cursor.execute("LOAD DATA INFILE %s INTO TABLE samples FIELDS TERMINATED BY '<SEP>' (user_id, song_id, date_val, date_id);", (file_path,))

    # Add indexes on samples
    cursor.execute("CREATE OR REPLACE INDEX samples_song_id_index ON samples (song_id);")

    mariadb_connection.commit()
    mariadb_connection.close()
    print('Execution time', time() - start)


if __name__ == "__main__":
    main()
