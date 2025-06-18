import random
import string
import json


def generate_alphabetic_data(num_entries, min_length, max_length):
    """generates Dataset with only upper and lower case letters (52 different chars)
        param: num_entries (int), min_length (int), max_length (int)
        return: one column the size of num_entries with random strings between min and max length long"""
    return [
        ''.join(random.choices(string.ascii_letters, k=random.randint(min_length, max_length)))
        for _ in range(num_entries)
    ]


def generate_numeric_data(num_entries, min_length, max_length):
    """generates Dataset with only numbers between 0 an 9
        param: num_entries (int), min_length (int), max_length (int)
        return: one column the size of num_entries with random numbers between min and max length long"""
    return [
        ''.join(random.choices(string.digits, k=random.randint(min_length, max_length)))
        for _ in range(num_entries)
    ]


def generate_printable_data(num_entries, min_length, max_length):
    """generates Dataset with all printable chars (100 different chars)
        param: num_entries (int), min_length (int), max_length (int)
        return: one column the size of num_entries with random strings between min and max length long"""
    return [
        ''.join(random.choices(string.printable, k=random.randint(min_length, max_length)))
        for _ in range(num_entries)
    ]


def generate_ascii_data(num_entries, min_length, max_length):
    """Generates a dataset with random words using all 256 ASCII characters.
        param: num_entries (int), min_length (int), max_length (int)
        return: one column the size of num_entries with random strings between min and max length long """
    ascii_chars = ''.join(map(chr, range(256)))  # All 256 ASCII characters
    return [
        ''.join(random.choices(ascii_chars, k=random.randint(min_length, max_length)))
        for _ in range(num_entries)
    ]


def generate_text_from_ascii_freq(num_entries, min_len, max_len, freq_path):
    """Generates a dataset with random words using all 256 ASCII characters.
        param: num_entries (int), min_length (int), max_length (int), freq_path (str)
        return: one column the size of num_entries with random strings between min and max length long """
    with open(freq_path, 'r') as f:
        data = json.load(f)

    ascii_codes = [entry["ascii"] for entry in data.values()]
    probabilities = [entry["frequency"] for entry in data.values()]

    entries = []
    for _ in range(num_entries):
        length = random.randint(min_len, max_len)
        codes = random.choices(ascii_codes, weights=probabilities, k=length)
        entry = ''.join(chr(code) for code in codes)
        entries.append(entry)

    return entries
