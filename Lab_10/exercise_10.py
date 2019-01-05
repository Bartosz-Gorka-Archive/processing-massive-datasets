import csv
from bitstring import BitArray
from collections import Counter

SOURCE_FILE_NAME = 'facts2.csv'
NEAREST_NEIGHBOR_SIZE = 100
MAX_SONG_ID = 999056 + 1  # TODO replace


def jaccard(bitarray_a, bitarray_b):
    min_one_of = bitarray_a.copy()
    min_one_of |= bitarray_b

    both = bitarray_a.copy()
    both &= bitarray_b

    total_objects = min_one_of.count(True)

    if total_objects > 0:
        return both.count(True) / total_objects
    else:
        return 0.0


def calculate_similarity(similarity, songs, max_user_id):
    for (user_id, my_song_list) in songs.items():
        print(user_id)
        for partner_user_id in range(user_id + 1, max_user_id + 1):
            partner_songs_list = songs.get(partner_user_id, [])
            similarity_value = jaccard(my_song_list, partner_songs_list)
            print(partner_user_id)

            # Set my similarity with partner - his/her stats
            partner_similarity_list = similarity.get(partner_user_id, [])
            partner_similarity_list.append([user_id, similarity_value])
            similarity.update({partner_user_id: partner_similarity_list})

            # Similarity - my stats
            my_similarity_list = similarity.get(user_id, [])
            my_similarity_list.append([partner_user_id, similarity_value])
            similarity.update({user_id: my_similarity_list})


def sort_by_similarity(similarity_list):
    return sorted(similarity_list, key=lambda record: record[1], reverse=True)


def nearest_neighbors(similarity):
    f = open('stats.txt', 'a')
    for (user_id, list_of_partners_similarity) in similarity.items():
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
            song_id = int(record[1])

            # If previous user is the same - append song to list
            if user_id == previous_user_id:
                user_songs_ids.append(song_id)
            else:
                # New user - we must store list of song ids, run calculations and start new group
                if previous_user_id != 0:
                    bitmap = BitArray(MAX_SONG_ID)
                    bitmap.set(True, user_songs_ids)
                    user_songs_groups.update({previous_user_id: bitmap})

                print(user_id)
                previous_user_id = user_id
                user_songs_ids = [song_id]

        bitmap = BitArray(MAX_SONG_ID)
        bitmap.set(True, user_songs_ids)
        user_songs_groups.update({previous_user_id: bitmap})

        print('BUILT!')
        calculate_similarity(user_similarity, user_songs_groups, previous_user_id)
        nearest_neighbors(user_similarity)


if __name__ == '__main__':
    main()
