import csv
from numpy import sum as np_sum

SOURCE_FILE_NAME = 'facts3.csv'
NEAREST_NEIGHBOR_SIZE = 100


def jaccard(list_a, list_b):
    # List stored 'hit' in song_id - no zeros in both records
    # When value in one or both lists - we are sure this value can be used in Jaccard Index
    intersection_count = 0
    length_list_a = len(list_a)
    length_list_b = len(list_b)

    # Search based on shorter list
    if length_list_a < length_list_b:
        for value in list_a:
            if value in list_b:
                intersection_count += 1
    else:
        for value in list_b:
            if value in list_a:
                intersection_count += 1

    return intersection_count / (length_list_a + length_list_b - intersection_count)


def calculate_similarity(similarity, songs):
    for (user_id, my_song_list) in songs.items():
        if user_id > 100:
            break

        my_similarity_list = similarity.get(user_id, [])

        for (partner_id, partner_songs_list) in songs.items():
            similarity_value = jaccard(my_song_list, partner_songs_list)

            if similarity_value > 0:
                my_similarity_list.append([partner_id, similarity_value])

        # Store updated stats
        similarity[user_id] = my_similarity_list


def sort_by_similarity(similarity_list):
    return sorted(similarity_list, key=lambda record: (record[1], record[0]), reverse=True)


def nearest_neighbors(similarity):
    f = open('example.txt', 'w+')
    for user_id in sorted(similarity.keys()):
        list_of_partners_similarity = similarity[user_id];
        if user_id > 100:
            break

        f.write(f'User = {user_id}\n')
        [f.write('{:8d} {:7.5f}\n'.format(record[0], record[1])) for record in sort_by_similarity(list_of_partners_similarity)[0:NEAREST_NEIGHBOR_SIZE-1]]

    f.close()


def main():
    with open(SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        # Skip header with fields
        next(reader, None)

        user_songs_groups = {}
        user_similarity = {}

        print('START')
        for record in reader:
            # Fist value in record is a `user_id`, second - `song_id`
            user_id = int(record[0])
            song_id = int(record[1])

            # Sets for speed-up calculations
            if user_id in user_songs_groups:
                user_songs_groups[user_id].add(song_id)
            else:
                user_songs_groups[user_id] = {song_id}

        print('CALCULATE SIMILARITY')
        calculate_similarity(user_similarity, user_songs_groups)
        print('NEIGHBORS')
        nearest_neighbors(user_similarity)
        print('FINISH')


if __name__ == '__main__':
    main()
