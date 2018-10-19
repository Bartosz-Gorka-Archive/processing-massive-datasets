import numpy as np
import itertools

NUMBER_OF_PEOPLE = 10000
PROBABILITY = 0.1
NUMBER_OF_HOTELS = 100
NUMBER_OF_DAYS = 100


def main():
    # Dict - pairs
    potential_terrorist_pairs = {}

    # Dict - statistics
    meetings_stats = {}
    terrorist_days = 0
    unique_terrorist = set()

    # We should simulate daily choice
    for day in range(NUMBER_OF_DAYS):
        print(f'DAY {day}')

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


if __name__ == '__main__':
    main()
