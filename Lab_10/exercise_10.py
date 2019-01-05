import csv

SOURCE_FILE_NAME = 'facts.csv'


def main():
    with open(SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        # Skip header with fields
        next(reader, None)

        user_songs_groups = {}

        previous_user_id = None
        user_songs_ids = []

        for record in reader:
            # Fist value in record is a `user_id`, second - `song_id`
            user_id = int(record[0])
            song_id = int(record[1])

            # If previous user is the same - append song to list
            if user_id == previous_user_id:
                user_songs_ids.append(song_id)
            else:
                # New user - we must store list of song ids, run calculations and start new group
                user_songs_groups.update({previous_user_id: user_songs_ids})
                # TODO calculations

                previous_user_id = user_id
                user_songs_ids = [song_id]

        user_songs_groups.update({previous_user_id: user_songs_ids})
        # TODO calculations

        print('FINAL')
        for (key, value) in user_songs_groups.items():
            print(key, value)


if __name__ == '__main__':
    main()
