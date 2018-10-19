import numpy as np
import itertools

NUMBER_OF_PEOPLE = 10000
PROBABILITY = 0.1
NUMBER_OF_HOTELS = 100
NUMBER_OF_DAYS = 100


def main():
    # We should simulate daily choice
    for day in range(NUMBER_OF_DAYS):
        print(f'DAY {day}:')

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
            print(guests_combinations)


if __name__ == '__main__':
    main()
