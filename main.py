import numpy as np
import itertools

NUMBER_OF_PEOPLE = 10000
PROBABILITY = 0.1
NUMBER_OF_HOTELS = 100
NUMBER_OF_DAYS = 100
NUMBER_OF_STATS_ITERATIONS = 1000
DISPLAY_ITERATIONS = True


def main():
    f = open('stats.txt', 'a')
    # Loop with stats - variables
    unique_terrorist_cardinality_list = []
    terrorist_days_cardinality_list = []
    meetings_stats_list = []

    for iteration in range(NUMBER_OF_STATS_ITERATIONS):
        print(f'Iteration {iteration}')
        f.write(f'Iteration {iteration}\n')
        # Dict - pairs
        potential_terrorist_pairs = {}

        # Dict - statistics
        meetings_stats = np.zeros(10)
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
            meetings_stats[cardinality] += 1
            if cardinality >= 2:
                terrorist_days += len(list(itertools.combinations(range(cardinality), 2)))
                for person_id in pair.split('-'):
                    unique_terrorist.add(person_id)

        # Display results when enabled
        if DISPLAY_ITERATIONS:
            f.write(f'Terrorist * day = {terrorist_days}\n')
            f.write(f'Unique terrorist count = {len(unique_terrorist)}\n')
            f.write('Histogram stats\n')
            for (key, val) in enumerate(meetings_stats):
                if val > 0:
                    f.write(f'\t{key}: {val}\n')

        # Append values from current iteration to main stats params
        unique_terrorist_cardinality_list.append(len(unique_terrorist))
        terrorist_days_cardinality_list.append(terrorist_days)
        meetings_stats_list.append(meetings_stats)

    # Calculate and display stats
    f.write('\nTerrorist * day\n')
    f.write(f'\tMIN: {np.min(terrorist_days_cardinality_list)}\n')
    f.write(f'\tAVERAGE: {np.average(terrorist_days_cardinality_list)}\n')
    f.write(f'\tMEDIAN: {np.median(terrorist_days_cardinality_list)}\n')
    f.write(f'\tMAX: {np.max(terrorist_days_cardinality_list)}\n')

    f.write('\nUnique terrorist count\n')
    f.write(f'\tMIN: {np.min(unique_terrorist_cardinality_list)}\n')
    f.write(f'\tAVERAGE: {np.average(unique_terrorist_cardinality_list)}\n')
    f.write(f'\tMEDIAN: {np.median(unique_terrorist_cardinality_list)}\n')
    f.write(f'\tMAX: {np.max(unique_terrorist_cardinality_list)}\n')

    histogram_stats = {}
    for record in meetings_stats_list:
        for (key, val) in enumerate(record):
            visits = histogram_stats.get(key, [])
            visits.append(val)
            histogram_stats.update({key: visits})

    f.write('\nHistogram stats\n')
    for (key, val) in histogram_stats.items():
        max_value = np.max(val)
        if max_value > 0:
            f.write(f'\t{key}: MIN {np.min(val)} \t| AVG {np.average(val)} \t| MEDIAN {np.median(val)}' +
                    f'\t| MAX {max_value}\n')


if __name__ == '__main__':
    main()
