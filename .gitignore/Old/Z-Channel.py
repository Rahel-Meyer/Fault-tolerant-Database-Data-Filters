import random


### Not used anymore

def z_channel_prefix(prefix_list, error_probability):
    """Corrupts prefixes based on error probability (flips 1 -> 0 only).
    Param: Prefix list (list[str]), Error probability (float)
    Return: Corrupted prefix list, number of bit flips"""

    corrupted_prefix_list = []
    flip_count = 0

    for prefix in prefix_list:
        corrupted_prefix = ""

        for char in prefix:
            binary_char = format(ord(char), '08b')
            corrupted_binary_char = []

            for bit in binary_char:
                if bit == '1' and random.random() < error_probability:
                    corrupted_binary_char.append('0')
                    flip_count += 1
                else:
                    corrupted_binary_char.append(bit)

            corrupted_char = chr(int(''.join(corrupted_binary_char), 2))
            corrupted_prefix += corrupted_char

        corrupted_prefix_list.append(corrupted_prefix)

    return corrupted_prefix_list, flip_count


def reverse_z_channel_prefix(prefix_list, error_probability):
    """Corrupts prefixes based on error probability (flips 0 -> 1 only).
    Param: Prefix list (list[str]), Error probability (float)
    Return: Corrupted prefix list, number of bit flips"""

    corrupted_prefix_list = []
    flip_count = 0

    for prefix in prefix_list:
        corrupted_prefix = ""

        for char in prefix:
            binary_char = format(ord(char), '08b')
            corrupted_binary_char = []

            for bit in binary_char:
                if bit == '0' and random.random() < error_probability:
                    corrupted_binary_char.append('1')
                    flip_count += 1
                else:
                    corrupted_binary_char.append(bit)

            corrupted_char = chr(int(''.join(corrupted_binary_char), 2))
            corrupted_prefix += corrupted_char

        corrupted_prefix_list.append(corrupted_prefix)

    return corrupted_prefix_list, flip_count


def evaluate_Confusionmatrix_old(corrupted_filter, correct_filter, data, n):
    """Evaluates confusion matrix values for a corrupted filter compared to the correct filter.
    Here the indexes are compared so an FP is where the corrupt filter answers yes and the correct one at the same Index no.
    param: corrupted and correct Filter for comparison, data to check, n=size of Prefixes
    return: TP, TN, FP, FN"""
    data_prefixes = [item.split('|')[0][:n] for item in data if item]

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for data_prefix in data_prefixes:
        matched = False
        TP_found = False
        for idx, prefix_corrupt in enumerate(corrupted_filter):
            if data_prefix == prefix_corrupt:
                if prefix_corrupt == correct_filter[idx]:
                    true_positives += 1
                    TP_found = True
                    break
                else:
                    matched = True
        if matched and not TP_found:
            false_positives += 1
        if not matched and not TP_found:
            if data_prefix in correct_filter:
                false_negatives += 1
            else:
                true_negatives += 1

    return true_positives, true_negatives, false_positives, false_negatives
