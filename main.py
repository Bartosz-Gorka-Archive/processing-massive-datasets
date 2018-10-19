import numpy as np

NUMBER_OF_PEOPLE = 10000
PROBABILITY = 0.1
NUMBER_OF_HOTELS = 100
NUMBER_OF_DAYS = 100


def main():
    # We should simulate daily choice
    for day in range(NUMBER_OF_DAYS):
        print(f'DAY {day}:')
        # We should simulate each person
        for person_id in range(NUMBER_OF_PEOPLE):
            # Check random decision - visit hotel or not
            if np.random.random_sample() < PROBABILITY:
                # Guest decided visit hotel - should check which
                hotel_id = np.random.randint(0, NUMBER_OF_HOTELS)
                print(f'Guest {person_id} visit {hotel_id}')


if __name__ == '__main__':
    main()
