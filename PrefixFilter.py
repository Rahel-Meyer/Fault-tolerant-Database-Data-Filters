import random
import string
from collections import defaultdict


def cal_prefix(data, k):
    """ Calculates prefixes from a table of one column.
        param: Data (list[])
        param: k (int), length of prefixes
        return: dictionary of different Prefixes with reference to data"""

    prefixes = defaultdict(list)

    for item in data:
        if len(item) >= k:
            prefix = item.split('|')[0][:k]
            prefixes[prefix].append(item)

    return dict(prefixes)


def corrupt_filter(prefix_dic, error_probability, b):
    """Corrupts prefixes in dictionary based on error probability (flips 1s and 0s).
        param: Prefix dictionary (list[prefix][values])
        param: error_probability (float)
        param: b (int), number of bits per character
        Return: corrupted filter (dictionary)"""

    corrupted_prefix_dic = defaultdict(list)
    invalid = 0
    M = 32 ** 2

    for prefix, values in prefix_dic.items():
        if b == 5:
            corrupted_prefix = corrupt_prefix_5(prefix, error_probability, b)
        else:
            corrupted_prefix = corrupt_prefix_8(prefix, error_probability, b)

        inv = False
        for char in corrupted_prefix:
            if char not in string.ascii_lowercase:
                inv = True
        if inv:
            invalid += 1
        corrupted_prefix_dic[corrupted_prefix].extend(values)

    return corrupted_prefix_dic, invalid / M


def corrupt_prefix_5(prefix, error_probability, b):
    """flips bits based on error probability for b=5
        param: prefix (string)
        param: error_probability (float)
        param: b (int), number of bits per character
        return: prefix (string)"""

    corrupted_prefix = ""
    for char in prefix:
        binary_char = format(ord(char), f'0{b}b')
        corrupted_binary_char = []

        for index, bit in enumerate(binary_char):
            # binary_char has 7 bits but should have 5
            if index < 2:  # skip first two bits
                corrupted_binary_char.append(bit)  # Keep them unchanged
            else:
                if bit == '0' and random.random() < error_probability:
                    corrupted_binary_char.append('1')
                elif bit == '1' and random.random() < error_probability:
                    corrupted_binary_char.append('0')
                else:
                    corrupted_binary_char.append(bit)

        corrupted_char = chr(int(''.join(corrupted_binary_char), 2))
        corrupted_prefix += corrupted_char
    return corrupted_prefix


def corrupt_prefix_8(prefix, error_probability, b):
    """flips bits based on error probability
        param: prefix (string)
        param: error_probability (float)
        param: b (int), number of bits per character
        return: prefix (string)"""

    corrupted_prefix = ""
    for char in prefix:
        binary_char = format(ord(char), f'0{b}b')
        corrupted_binary_char = []

        for bit in binary_char:
            if bit == '0' and random.random() < error_probability:
                corrupted_binary_char.append('1')
            elif bit == '1' and random.random() < error_probability:
                corrupted_binary_char.append('0')
            else:
                corrupted_binary_char.append(bit)

        corrupted_char = chr(int(''.join(corrupted_binary_char), 2))
        corrupted_prefix += corrupted_char
    return corrupted_prefix


def evaluate_Confusionmatrix(corrupted_filter_dic, prefixes, k, b):
    """Evaluates confusion matrix values for a corrupted filter compared to the original filter.
        param: corrupted filter (dictionary)
        param: prefixes (dictionary), original filter
        param: k (int), length of prefixes
        param: b (int), number of bits per character
        return: TP (int), TN (int), FP (int), FN (int)"""
    keys = corrupted_filter_dic.keys()

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    characters = 2 ** b
    M = characters ** k

    for prefix in keys:
        value_prefix = corrupted_filter_dic[prefix][0].split('|')[0][:k]
        if prefix == value_prefix:
            true_positives += 1
        else:
            false_positives += 1

    for prefix in prefixes:
        if prefix not in keys:
            false_negatives += 1

    true_negatives = M - true_positives - false_negatives - false_positives

    return true_positives / M, true_negatives / M, false_positives / M, false_negatives / M


def iteration_filter(data, error_probabilities, k, b):
    """One iteration of corrupting the filter and counting the confusion matrix for the error probabilities.
        param: Data (list[])
        param: error_probabilities (list[])
        param: k (int), length of prefixes
        param: b (int), number of bits per character
        return: TP list[], TN list[], FP list[], FN list[]"""

    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    prefixes = cal_prefix(data, k)
    inf = []  # has beem used to count number of invalids

    for error_probability in error_probabilities:
        corrupted_prefixes, invalid = corrupt_filter(prefixes, error_probability, b)
        TP, TN, FP, FN = evaluate_Confusionmatrix(corrupted_prefixes, prefixes, k, b)

        fp_results.append(FP)
        fn_results.append(FN)
        tp_results.append(TP)
        tn_results.append(TN)
        inf.append(0)  # no use anymore

    return tp_results, tn_results, fp_results, fn_results, inf
