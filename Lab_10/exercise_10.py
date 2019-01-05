import csv
from collections import Counter

SOURCE_FILE_NAME = 'facts2.csv'


def jaccard(list_a, list_b):
    # List stored 'hit' in song_id - no zeros in both records
    # When value in one or both lists - we are sure this value can be used in Jaccard Index
    all_elements_list = list_a + list_b
    elements_cardinality = Counter(all_elements_list).values()

    total_objects = len(elements_cardinality)
    the_same = len(list(filter(lambda x: x == 2, elements_cardinality)))

    if total_objects > 0:
        return the_same / total_objects
    else:
        return 0.0


def calculate_similarity(similarity, songs, user_id):
    # Fetch from songs our record (list listened songs)
    my_song_ids = songs.get(user_id)
    print(user_id)

    # Run in loop Jaccard calculations - skip our record
    for (partner_user_id, partner_songs_list) in songs.items():
        similarity_value = jaccard(my_song_ids, partner_songs_list)

        # TODO - verify sort by value and change structure
        # Set my similarity with partner - his/her stats
        partner_similarity_list = similarity.get(partner_user_id, [])
        partner_similarity_list.append([user_id, similarity_value])
        similarity.update({partner_user_id: partner_similarity_list})

        # Similarity - my stats
        my_similarity_list = similarity.get(user_id, [])
        my_similarity_list.append([partner_user_id, similarity_value])
        similarity.update({user_id: my_similarity_list})


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
                # To speed up calculations we should make songs unique
                user_songs_ids = list(set(user_songs_ids))
                user_songs_groups.update({previous_user_id: user_songs_ids})
                calculate_similarity(user_similarity, user_songs_groups, previous_user_id)

                previous_user_id = user_id
                user_songs_ids = [song_id]

        # To speed up calculations we should make songs unique
        user_songs_ids = list(set(user_songs_ids))
        user_songs_groups.update({previous_user_id: user_songs_ids})
        calculate_similarity(user_similarity, user_songs_groups, previous_user_id)

        print('FINAL')
        for (key, value) in user_similarity.items():
            print(key, value)


if __name__ == '__main__':
    main()
