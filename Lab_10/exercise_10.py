import csv
from itertools import chain
from collections import Counter

SOURCE_FILE_NAME = 'facts3.csv'
NEAREST_NEIGHBOR_SIZE = 100


def jaccard(list_a, list_b):
    # List stored 'hit' in song_id - no zeros in both records
    # When value in one or both lists - we are sure this value can be used in Jaccard Index
    all_elements_list = chain(list_b, list_a)

    # all_elements_list = list_a + list_b
    elements_cardinality = Counter(all_elements_list).values()

    total_objects = len(elements_cardinality)
    the_same = len(list(filter(lambda x: x == 2, elements_cardinality)))

    if total_objects > 0:
        return the_same / total_objects
    else:
        return 0.0


def calculate_similarity(similarity, songs, max_user_id):
    for (user_id, my_song_list) in songs.items():
        if user_id > 100:
            continue
        print(user_id)
        my_similarity_list = similarity.get(user_id, [])

        for partner_user_id in range(user_id + 1, max_user_id + 1):
            partner_songs_list = songs.get(partner_user_id, [])
            similarity_value = jaccard(my_song_list, partner_songs_list)

            if partner_user_id <= 100:
                # Set my similarity with partner - his/her stats
                partner_similarity_list = similarity.get(partner_user_id, [])
                partner_similarity_list.append([user_id, similarity_value])
                similarity[partner_user_id] = partner_similarity_list

            # Similarity - my stats
            my_similarity_list.append([partner_user_id, similarity_value])

        # Store updated stats
        similarity[user_id] = my_similarity_list


def sort_by_similarity(similarity_list):
    return sorted(similarity_list, key=lambda record: record[1], reverse=True)


def nearest_neighbors(similarity):
    f = open('stats.txt', 'w+')
    for user_id in sorted(similarity.keys()):
        list_of_partners_similarity = similarity[user_id];
        if user_id > 100:
            continue

        f.write(f'User = {user_id}\n')
        f.write('{:8d} 1.00000\n'.format(user_id))
        for record in sort_by_similarity(list_of_partners_similarity)[0:NEAREST_NEIGHBOR_SIZE]:
            if record[1] > 0:
                f.write('{:8d} {:7.5f}\n'.format(record[0], record[1]))
    f.close()


def main():
    with open(SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        # Skip header with fields
        next(reader, None)

        user_songs_groups = {}
        user_similarity = {}

        previous_user_id = 0
        user_songs_ids = []

        for record in reader:
            # Fist value in record is a `user_id`, second - `song_id`
            user_id = int(record[0])
            song_id = record[1]

            # If previous user is the same - append song to list
            if user_id == previous_user_id:
                user_songs_ids.append(song_id)
            else:
                # New user - we must store list of song ids, run calculations and start new group
                if previous_user_id != 0:
                    user_songs_ids = list(set(user_songs_ids))
                    user_songs_groups[previous_user_id] = user_songs_ids

                previous_user_id = user_id
                user_songs_ids = [song_id]

        user_songs_ids = list(set(user_songs_ids))
        user_songs_groups[previous_user_id] = user_songs_ids

        print('BUILT!')
        calculate_similarity(user_similarity, user_songs_groups, previous_user_id)
        print('SORT AND STORE!')
        nearest_neighbors(user_similarity)
        print('FINISH')


if __name__ == '__main__':
    main()
