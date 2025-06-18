from bitarray import bitarray
import hashlib
import random


def bloom_hash(data, size):
    bit_array = bitarray(size)
    bit_array.setall(0)
    with open(data, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                hash_result = hashlib.sha256(line.encode()).hexdigest()
                index = int(hash_result, 16) % size
                bit_array[index] = 1

    return bit_array


def bloom_check(checkarray, item, size):
    item = item.strip()
    hash_result = hashlib.sha256(item.encode()).hexdigest()
    index = int(hash_result, 16) % size
    return checkarray[index] == 1


def bloom_size(data):
    with open(data, 'r', encoding='utf-8') as file:
        size = sum(1 for line in file)
    return size


def z_channel_bloom(bitarray, error_probability):
    corrupted_bitarray = bitarray[:]
    for i in range(len(corrupted_bitarray)):
        if corrupted_bitarray[i] == 1 and random.random() < error_probability:
            corrupted_bitarray[i] = 0
    return corrupted_bitarray


def test_multiple_files(error_propability):
    data_paths = [
        'tpch-data/nation.tbl/nation.tbl',
        'tpch-data/customer.tbl/customer.tbl',
        'tpch-data/orders.tbl/orders.tbl',
        'tpch-data/part.tbl/part.tbl',
        'tpch-data/partsupp.tbl/partsupp.tbl',
        'tpch-data/region.tbl/region.tbl',
        'tpch-data/supplier.tbl/supplier.tbl'
    ]

    result = []
    for data_path in data_paths:
        # test_correct_filter(data_path)
        result.append(test_corrupted_filter(data_path, error_propability))

    return result


def test_correct_filter(data):
    size = bloom_size(data)
    bloom = bloom_hash(data, size)

    total_items = 0
    false_negatives = 0

    with open(data, 'r', encoding='utf-8') as file:
        for line in file:
            if not bloom_check(bloom, line, size):
                return False
            else:
                total_items = +1

    true_positives = total_items
    return total_items, false_negatives, true_positives


def test_corrupted_filter(data, error_probability):
    size = bloom_size(data)
    bloom = bloom_hash(data, size)
    corrupt_bloom = z_channel_bloom(bloom, error_probability)

    total_items = 0
    false_negatives = 0

    with open(data, 'r', encoding='utf-8') as file:
        for line in file:
            total_items += 1
            if not bloom_check(corrupt_bloom, line, size):
                false_negatives += 1

    true_positives = total_items - false_negatives
    '''print("Total Items", total_items)
    print("False Negatives", false_negatives)
    print("True Positives", true_positives)'''

    return total_items, false_negatives, true_positives
