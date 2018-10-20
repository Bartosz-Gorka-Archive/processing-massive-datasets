import numpy as np
import itertools
import collections

NUMBER_OF_PEOPLE = 10000
PROBABILITY = 0.1
NUMBER_OF_HOTELS = 100
NUMBER_OF_DAYS = 100
NUMBER_OF_STATS_ITERATIONS = 10
DISPLAY_ITERATIONS = False


def main():
    # Loop with stats - variables
    unique_terrorist_cardinality_list = []
    terrorist_days_cardinality_list = []
    meetings_stats_list = []

    for iteration in range(NUMBER_OF_STATS_ITERATIONS):
        print(f'Iteration {iteration}')
        # Dict - pairs
        potential_terrorist_pairs = {}

        # Dict - statistics
        meetings_stats = {}
        terrorist_days = 0
        unique_terrorist = set()

        # We should simulate daily choice
        for day in range(NUMBER_OF_DAYS):
            # Dict - visit hotels in selected days
            visits_in_hotels = {}

            # We should simulate each person
            for person_id in range(NUMBER_OF_PEOPLE):
                # Check random decision - visit hotel or not
                if np.random.random_sample() < PROBABILITY:
                    # Guest decided visit hotel - should check which
                    hotel_id = np.random.randint(0, NUMBER_OF_HOTELS)

                    # Append person_id to guest ids in selected hotel
                    guest_ids = visits_in_hotels.get(hotel_id, [])
                    guest_ids.append(person_id)
                    visits_in_hotels.update({hotel_id: guest_ids})

            # Make combinations to connect person in pair
            for (hotel_id, guest_ids) in visits_in_hotels.items():
                guests_combinations = list(itertools.combinations(guest_ids, 2))

                # Update counters in pairs dict
                for (guest, partner) in guests_combinations:
                    key = f'{guest}-{partner}'
                    together_days = potential_terrorist_pairs.get(key, 0)
                    potential_terrorist_pairs.update({key: together_days + 1})

        # Calculate statistics
        for (pair, cardinality) in potential_terrorist_pairs.items():
            meetings_stats.update({cardinality: meetings_stats.get(cardinality, 0) + 1})
            if cardinality >= 2:
                terrorist_days += len(list(itertools.combinations(range(cardinality), 2)))
                for person_id in pair.split('-'):
                    unique_terrorist.add(person_id)

        # Order histogram stats
        ordered_stats = collections.OrderedDict(sorted(meetings_stats.items()))

        # Display results when enabled
        if DISPLAY_ITERATIONS:
            print(f'Terrorist * day = {terrorist_days}')
            print(f'Unique terrorist count = {len(unique_terrorist)}')
            print('Histogram stats')
            for (key, val) in ordered_stats.items():
                print(f'\t{key}: {val}')

        # Append values from current iteration to main stats params
        unique_terrorist_cardinality_list.append(len(unique_terrorist))
        terrorist_days_cardinality_list.append(terrorist_days)
        meetings_stats_list.append(ordered_stats)

    # Calculate and display stats
    print('\nTerrorist * day')
    print(f'\tMIN: {np.min(terrorist_days_cardinality_list)}')
    print(f'\tAVERAGE: {np.average(terrorist_days_cardinality_list)}')
    print(f'\tMEDIAN: {np.median(terrorist_days_cardinality_list)}')
    print(f'\tMAX: {np.max(terrorist_days_cardinality_list)}')

    print('\nUnique terrorist count')
    print(f'\tMIN: {np.min(unique_terrorist_cardinality_list)}')
    print(f'\tAVERAGE: {np.average(unique_terrorist_cardinality_list)}')
    print(f'\tMEDIAN: {np.median(unique_terrorist_cardinality_list)}')
    print(f'\tMAX: {np.max(unique_terrorist_cardinality_list)}')

    histogram_stats = {}
    for dictionary in meetings_stats_list:
        for (key, val) in dictionary.items():
            visits = histogram_stats.get(key, [])
            visits.append(val)
            histogram_stats.update({key: visits})

    print('\nHistogram stats')
    for (key, val) in histogram_stats.items():
        print(f'\t{key}: MIN {np.min(val)} \t| AVG {np.average(val)} \t| MEDIAN {np.median(val)} \t| MAX {np.max(val)}')


if __name__ == '__main__':
    main()
