import csv
from itertools import combinations

SOURCE_FILE_NAME = 'facts.csv'
NEAREST_NEIGHBOR_SIZE = 100


def sort_by_similarity(similarity_list):
    return sorted(similarity_list, key=lambda record: (record[1], record[0]), reverse=True)


def nearest_neighbors(similarity):
    f = open('wyniktotal.txt', 'w+')
    for user_id in sorted(similarity.keys()):
        list_of_partners_similarity = similarity[user_id]

        f.write(f'User = {user_id}\n')
        f.write('{:8d} 1.00000\n'.format(user_id)) # I know - this is a hack
        [f.write('{:8d} {:7.5f}\n'.format(record[0], record[1])) for record in sort_by_similarity(list_of_partners_similarity)[0:NEAREST_NEIGHBOR_SIZE-1]]

    f.close()


def main():
    with open(SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        # Skip header with fields
        next(reader, None)

        songs_groups = {}
        user_song_count = {}
        hist_dict = {}
        similarity = {}

        print('START')
        for record in reader:
            song_id = int(record[1])
            if song_id in songs_groups:
                songs_groups[song_id].add(int(record[0]))
            else:
                songs_groups[song_id] = {int(record[0])}

        print('CALCULATE HITS')
        print(len(songs_groups))
        row = 0
        for song_id, unique_users_ids in songs_groups.items():
            print(row, len(unique_users_ids))
            row += 1

            for user_id in unique_users_ids:
                # Store +1 in user's songs
                user_song_count[user_id] = user_song_count.get(user_id, 0) + 1

            for (user_1, user_2) in combinations(unique_users_ids, 2):
                if user_1 > 100 and user_2 > 100:
                    continue

                if user_1 < user_2:
                    key = f'{user_1}-{user_2}'
                else:
                    key = f'{user_2}-{user_1}'
                hist_dict[key] = hist_dict.get(key, 0) + 1

        print('SIMILARITY')
        for (key, hits) in hist_dict.items():
            user_ids = key.split('-')
            user_1 = int(user_ids[0])
            user_2 = int(user_ids[1])

            total = user_song_count[user_1] + user_song_count[user_2]
            value = hits / (total - hits)

            similar = similarity.get(user_1, [])
            similar.append([user_2, value])
            similarity[user_1] = similar

            similar = similarity.get(user_2, [])
            similar.append([user_1, value])
            similarity[user_2] = similar

        print('SAVE')
        nearest_neighbors(similarity)

        print('FINISH')


if __name__ == '__main__':
    main()
