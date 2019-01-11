import csv
from heapq import heappush, heappushpop

SOURCE_FILE_NAME = 'facts2.csv'
NEAREST_NEIGHBOR_SIZE = 100
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


def calculate_similarity(similarity, songs):
    for (user_id, my_song_list) in songs.items():
        # For now only first 100 users
        if user_id > 100:
            break

        my_similarity_list = similarity.get(user_id, [])

        # Calculate Jaccard Index with all partners
        for (partner_id, partner_songs_list) in songs.items():
            similarity_value = jaccard(my_song_list, partner_songs_list)

            # Add only when greater than zero
            if similarity_value > 0:
                if len(my_similarity_list) < NEAREST_NEIGHBOR_SIZE:
                    heappush(my_similarity_list, [similarity_value, partner_id])
                else:
                    heappushpop(my_similarity_list, [similarity_value, partner_id])

        # Store updated stats
        similarity[user_id] = my_similarity_list


def sort_by_similarity(similarity_list):
    # Sort first by value, when conflicts - user_id
    return sorted(similarity_list, key=lambda record: (record[0], record[1]), reverse=True)


def nearest_neighbors(similarity):
    f = open('RESULTS_100.txt', 'w+')
    for user_id in sorted(similarity.keys()):
        # Store only first 100 users
        if user_id > NEAREST_NEIGHBOR_SIZE:
            break

        list_of_partners_similarity = similarity[user_id];
        f.write(f'User = {user_id}\n')
        [f.write('{:8d} {:7.5f}\n'.format(record[1], record[0])) for record in sort_by_similarity(list_of_partners_similarity)[0:NEAREST_NEIGHBOR_SIZE]]

    f.close()


# TODO list
# - minhash similarity
# - build structure with user_id: hashed song_id list
# - hash song_id -> minhashes
# - build structure set of song_id, next dictionary with hashes
# - prime number search
# - hash functions - generate list of parameters a, b
# - RMSE function
# - compare results and calculate RMSE
# - generate statistics in loop
# - prepare raport - graphs

def main():
    x = minhash_similarity([1, 2, 3], [3, 2, 1], 3)
    print(x)
    # with open(SOURCE_FILE_NAME, 'r') as f:
    #     reader = csv.reader(f)
    #     # Skip header with fields
    #     next(reader, None)
    #
    #     user_songs_groups = {}
    #     user_similarity = {}
    #
    #     print('START')
        # for record in reader:
        #     # Fist value in record is a `user_id`, second - `song_id`
        #     user_id = int(record[0])
        #     song_id = int(record[1])
        #
        #     # Sets for speed-up calculations
        #     if user_id in user_songs_groups:
        #         user_songs_groups[user_id].add(song_id)
        #     else:
        #         user_songs_groups[user_id] = {song_id}
        #
        # print('CALCULATE SIMILARITY')
        # calculate_similarity(user_similarity, user_songs_groups)
        # print('NEIGHBORS')
        # nearest_neighbors(user_similarity)
        # print('FINISH')


if __name__ == '__main__':
    main()
