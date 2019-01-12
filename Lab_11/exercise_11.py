import csv
from time import clock # TODO REMOVE
from math import sqrt
from numpy import min as np_min
from random import randint
from sympy import nextprime
from heapq import heappush, heappushpop

SOURCE_FILE_NAME = 'facts.csv'
FIRST_N_USERS = 100
TOTAL_HASH_FUNCTIONS = 100


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


def minhash_similarity(list_a, list_b, length):
    # Both list with the same length (received as parameters to speed-up) calculations
    # We need verify only positions in both lists
    # Hit when a[x] == b[x]
    hits = 0

    for (val_a, val_b) in zip(list_a, list_b):
        if val_a == val_b:
            hits += 1

    return hits / length


def next_prime(n):
    return nextprime(n)


def generate_hash_functions(n):
    hash_functions = []
    prime = next_prime(n)

    for i in range(0, TOTAL_HASH_FUNCTIONS):
        a = randint(1, prime)
        b = randint(0, prime)
        hash_functions.append([a, b])

    return hash_functions, prime


def hash_value(value, prime, params):
    return (params[0] * value + params[1]) % prime;


def hash_song_ids(songs_ids_set, hash_functions, prime):
    songs = {}
    for song in songs_ids_set:
        songs[song] = [hash_value(song, prime, elem) for elem in hash_functions]

    return songs


def hash_user_history(user_songs_dict, hashed_songs):
    hashed_user_songs = {}
    for user_id, songs_list in user_songs_dict.items():
        print(user_id)
        signatures = [hashed_songs[song] for song in songs_list]

        results_list = []
        for i in range(0, TOTAL_HASH_FUNCTIONS):
            results_list.append(min(x[i] for x in signatures))

        hashed_user_songs[user_id] = results_list

    return hashed_user_songs


def calculate_minhash_similarity(hashed_user_songs):
    similarity = {}

    for user_id, my_song_list in hashed_user_songs.items():
        if user_id > FIRST_N_USERS:
            break
        print(user_id)

        my_similarity_list = []

        for partner_id, partner_songs_list in hashed_user_songs.items():
            similarity_value = minhash_similarity(my_song_list, partner_songs_list, TOTAL_HASH_FUNCTIONS)

            if similarity_value > 0:
                my_similarity_list.append([similarity_value, partner_id])

        # Store similarity result
        similarity[user_id] = my_similarity_list

    return similarity


def calculate_jaccard_similarity(users_songs):
    similarity = {}

    for user_id, my_song_list in users_songs.items():
        if user_id > FIRST_N_USERS:
            break
        print(user_id)

        my_similarity_dir = {}

        for partner_id, partner_songs_list in users_songs.items():
            similarity_value = jaccard(my_song_list, partner_songs_list)

            if similarity_value > 0:
                my_similarity_dir[partner_id] = similarity_value

        # Store similarity result
        similarity[user_id] = my_similarity_dir

    return similarity


def sort_by_similarity(similarity_list):
    # Sort first by value, when conflicts - user_id
    return sorted(similarity_list, key=lambda record: (record[0], record[1]), reverse=True)


def nearest_neighbors(similarity):
    f = open('RESULTS.txt', 'w+')
    for user_id in sorted(similarity.keys()):
        list_of_partners_similarity = similarity[user_id];
        f.write(f'User = {user_id}\n')
        [f.write('{:8d} {:7.5f}\n'.format(record[1], record[0])) for record in sort_by_similarity(list_of_partners_similarity)]

    f.close()


def error_single_user(minhash_list, jaccard_dir):
    list_length = len(minhash_list)
    if list_length == 0:
        return 0.0

    value = 0.0
    for record in minhash_list:
        value += pow(record[0] - jaccard_dir[record[1]], 2)

    return value / list_length


# TODO list
# - minhash - changed structure to dict, not list
# - error_single_user - based on jaccard, not minhash
# - fix store results in file after ^ changes
# - prepare raport - graphs

def main():
    with open(SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        # Skip header with fields
        next(reader, None)

        user_songs_groups = {}
        user_similarity = {}
        songs_ids_set = set()

        print('START')
        print(clock())

        for record in reader:
            # Fist value in record is a `user_id`, second - `song_id`
            user_id = int(record[0])
            song_id = int(record[1])

            # Sets for speed-up calculations
            if user_id in user_songs_groups:
                user_songs_groups[user_id].add(song_id)
            else:
                user_songs_groups[user_id] = {song_id}

            # Collect `song_id` - this should speed-up our calculations
            songs_ids_set.add(song_id)
        print('READ FINISHED')
        print(clock())

        max_song_id = max(songs_ids_set)
        hash_functions, prime = generate_hash_functions(max_song_id)
        hashed_songs_ids = hash_song_ids(songs_ids_set, hash_functions, prime)
        print(clock())
        hashed_user_songs = hash_user_history(user_songs_groups, hashed_songs_ids)
        print('STRUCTURES BUILT')
        print(clock())

        minhash_dict_similarity = calculate_minhash_similarity(hashed_user_songs)
        print('MINHASH SIMILARITY LIST BUILD')
        print(clock())

        jaccard_dict_similarity = calculate_jaccard_similarity(user_songs_groups)
        print('JACCARD SIMILARITY LIST BUILD')
        print(clock())

        rsme = 0.0
        for user_id, values in minhash_dict_similarity.items():
            rsme += error_single_user(values, jaccard_dict_similarity[user_id])
        print(sqrt(rsme))
        print(clock())

        nearest_neighbors(minhash_dict_similarity)
        print('FINISH')
        print(clock())

if __name__ == '__main__':
    main()
