import argparse
import csv
from faker import Faker
import names
from random import randint


def random_allergy():
    allergies = ['', '', 'PENICILLIN', 'PEANUTS', 'NKA', 'LATEX']
    x = randint(0, len(allergies) - 1)
    return allergies[x]


def rand_digits(n):
    return randint(10**(n-1), (10**n)-1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create a number of fake patients and output CSV"
    )

    parser.add_argument(
        'patients',
        type=int,
        default=50,
        help='The number patients to generate. By default we will split 50/50 m/f otherwise 49/51 m/f.',
    )

    args = parser.parse_args()

    fake_patients = []

    for fpg_id in range(1, args.patients + 1):
        dob = Faker().date_between(start_date='-80y', end_date='-18y')
        if fpg_id < ((args.patients + 1) / 2):
            first_name = names.get_first_name(gender='female')
            sex = 'F'
        else:
            first_name = names.get_first_name(gender='male')
            sex = 'M'
        
        last_name = names.get_last_name()

        fake_patients.append(
            {
                '%Name%': f'{last_name.upper()},{first_name.upper()}',
                '%Sex%': sex,
                '%Dob%': '{0:%m/%d/%Y}'.format(dob),
                '%Ssn%': f'{rand_digits(3)}-{rand_digits(2)}-{rand_digits(4)}',
                '%Allergies%': random_allergy()
            }
        )

    with open('fake-patients.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fake_patients[0].keys())
        w.writeheader()
        for fpt in fake_patients:
            w.writerow(fpt)
