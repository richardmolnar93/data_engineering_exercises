import random
import string
import re
from datetime import datetime

hyphen = "-" 
full_stop = "." # only considering these ^ as the rest will unnecessarily clutter the task at the expense of performance
characters = string.ascii_letters + string.digits + hyphen + full_stop


def generator(): 
        while True:
            ### Parameters added to ensure random distribution between character types. Aim for as low values as possible to ensure optimal performance.
            full_stop_likelihood_parameter = random.randint(1, 5) # adjust the interval if file extension generation takes too long
            hyphen_likelihood_parameter = random.randint(1, 5) # increase if iso-dates generation takes too long
            digits_likelihood_parameter = random.randint(1, 5) # increase if iso-dates generation takes too long
            letters_likelihood_parameter = random.randint(1, 5)
            ### ---
            weight_multipliers = [letters_likelihood_parameter] * (len(string.ascii_letters)) + [digits_likelihood_parameter] * (len(string.digits)) + [hyphen_likelihood_parameter] * (len(hyphen)) + [full_stop_likelihood_parameter] * (len(full_stop))
            random_string = ''.join(random.choices(characters, weights=weight_multipliers, k=random.randint(5, 15)))
            yield random_string

category_counts = {'Integers': 0, 'File Extensions': 0, 'ISO Dates': 0}

def apply_filters(string):
    filters = {
        'Integers': lambda x: x.isdigit(),
        'File Extensions': lambda x: x.endswith((".json", ".csv")),
        'ISO Dates': lambda x: is_iso_date(x)
    }
    for filter_name, filter_func in filters.items():
        if filter_func(string):
            print((string, filter_name)) # printing a tuple as a way to present categorisation inside the continuous output 
            category_counts[filter_name] += 1  # increment category count
            break # move onto the next string when match found

def is_iso_date(date_str):
    try:
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str): #since the line below would also pass 2020-1-1 format, which is not in line with requirements
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        else:
            return False
    except ValueError: # error triggered by the datetime parser if passed value does not match the expected pattern
        return False
    
def display_category_counts():
    print("\nCategory Counts:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")

gen = generator()
try:
        while True:
            _string = next(gen)
            apply_filters(_string)
except KeyboardInterrupt:  
        display_category_counts() # Easter egg: gives the information on how many items are in each category upon script termination