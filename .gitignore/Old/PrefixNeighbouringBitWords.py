from itertools import combinations
from random import sample
import math


def prefix_m_differences(prefix_filter, max_distance, num_flips):
    """Generates prefixes with up to `max_distance` additional 1s.
    param: prefix_filter (list[str]): List of original prefixes
    param: max_distance (int): Maximum number of bits to flip
    return: List of extended prefixes that have up to `max_distance` flipped bits
    """
    possible_results = set(prefix_filter)
    all_neighbors_by_distance = {d: set() for d in range(1, max_distance + 1)}
    for prefix in prefix_filter:
        binary_string = ''.join(format(ord(char), '08b') for char in prefix)
        bit_positions = list(range(len(binary_string)))
        for distance in range(1, max_distance + 1):
            for positions_to_flip in combinations(bit_positions, distance):
                flipped = list(binary_string)
                for pos in positions_to_flip:
                    flipped[pos] = '1' if flipped[pos] == '0' else '0'
                all_neighbors_by_distance[distance].add(''.join(flipped))

    neighbors_to_add = set()
    for distance in range(1, max_distance + 1):
        current_neighbors = []

        for binary_string in all_neighbors_by_distance[distance]:
            characters = []
            for i in range(0, len(binary_string), 8):
                byte = binary_string[i:i + 8]
                if len(byte) == 8:
                    char_code = int(byte, 2)
                    if 0 <= char_code < 128:
                        characters.append(chr(char_code))
                    else:
                        characters.append('?')  # Replace invalid chars
            current_neighbors.append(''.join(characters))

        if len(current_neighbors) + len(neighbors_to_add) > num_flips:
            remaining_space = int(num_flips - len(neighbors_to_add))
            neighbors_to_add.update(sample(current_neighbors, remaining_space))
            break
        neighbors_to_add.update(current_neighbors)

    return list(possible_results.union(neighbors_to_add))

def m_differences(data, data2, error_probabilities, n_value):
    """Calculates the Confusions matrix for the different error probabilities.
    param: Data (list[])
    param: data2 (list[])
    param: error_probabilities (list[])
    param: n_value (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""

    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    n = n_value
    prefix = PrefixFilter.prefix_set(data, n_value)
    num_characters = 52
    M = num_characters ** n
    u = len(data)
    P_U = M * (1 - (1 - 1 / M) ** u)

    for error_probability in error_probabilities:
        num_flips = round(len(prefix) * 8 * n * error_probability)
        prefixes = prefix_m_differences(data, 0, num_flips)
        corrupted_prefixes, _ = PrefixFilter.corrupt_set(prefixes, error_probability)
        TP, TN, FP, FN = PrefixFilter.evaluate_Confusionmatrix_set(corrupted_prefixes, prefixes, data2, n_value)

        fp_results.append(FP / P_U)
        fn_results.append(FN / P_U)
        tp_results.append(TP / P_U)
        tn_results.append(TN / P_U)

    return tp_results, tn_results, fp_results, fn_results

def prediction_neighbouring_bit_word(error_probabilities, u, v, n):
    """ Calculates the prediction for the Confusions matrix of the Filter with neighbouring bit words.
    param: error_probabilities (list[])
    param: u (int), length of data u
    param: v (int), length of data v
    param: n (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""

    pred_fp = []
    pred_fn = []
    pred_tp = []
    pred_tn = []

    num_characters = 100
    M = num_characters ** n
    P_U = M * (1 - (1 - 1 / M) ** u)
    P_V = M * (1 - (1 - 1 / M) ** v)
    apprx_num_positives = P_U * (1 - (1 - (1 / M)) ** u)
    apprx_num_negatives = P_U * (1 - (1 / M)) ** u

    u_union_v = M * (1 - (1 - (1 / M)) ** (u + v))
    u_intersect_v = P_U + P_V - u_union_v

    for p in error_probabilities:
        # for FP
        flip_negatives_to_v = apprx_num_negatives * (P_V / M) * (1 - (1 - p) ** (n * math.log(num_characters))) * (
                1 - (1 - (1 - p) ** (n * math.log(num_characters))))

        # for FN
        flip_positives_to_negatives = apprx_num_positives * ((M - u_intersect_v) / M) * (
                1 - (1 - p) ** (n * math.log(num_characters))) * (
                                              1 - (1 - (1 - p) ** (n * math.log(num_characters))))

        flip_positives_to_invalid = apprx_num_positives * (1 - (1 - p) ** (n * math.log(num_characters)))

        pred_FP = flip_negatives_to_v
        pred_FN = flip_positives_to_negatives + flip_positives_to_invalid

        pred_TP = apprx_num_positives - (flip_positives_to_negatives + flip_positives_to_invalid)
        pred_TN = apprx_num_negatives - flip_negatives_to_v

        pred_fp.append(pred_FP / P_U)
        pred_fn.append(pred_FN / P_U)
        pred_tp.append(pred_TP / P_U)
        pred_tn.append(pred_TN / P_U)

    return pred_tp, pred_tn, pred_fp, pred_fn

### Not used anymore

def prefix_m_more_1es(prefix_filter, max_distance):
    """Generates prefixes with up to `max_distance` additional 1s.
    param: prefix_filter (list[str]): List of original prefixes
    param: max_distance (int): Maximum number of bits to flip from 0 to 1
    return: List of extended prefixes that have up to `max_distance` flipped bits
    """
    possible_results = set()

    for prefix in prefix_filter:
        binary_string = ''.join(format(ord(char), '08b') for char in prefix)

        zero_positions = [i for i, bit in enumerate(binary_string) if bit == '0']

        for distance in range(1, max_distance + 1):
            for bit_positions in combinations(zero_positions, distance):
                flipped = list(binary_string)
                for pos in bit_positions:
                    flipped[pos] = '1'
                possible_results.add(''.join(flipped))

    possible_results_list = []
    for binary_string in possible_results:
        characters = []
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i + 8]
            if len(byte) == 8:
                char_code = int(byte, 2)
                if 0 <= char_code < 128:
                    characters.append(chr(char_code))
                else:
                    characters.append('?')
        possible_results_list.append(''.join(characters))

    return possible_results_list


def prefix_m_more_0es(prefix_filter, max_distance):
    """Generates prefixes with up to `max_distance` additional 1s.
    param: prefix_filter (list[str]): List of original prefixes
    param: max_distance (int): Maximum number of bits to flip from 1 to 0
    return: List of extended prefixes that have up to `max_distance` flipped bits
    """
    possible_results = set()

    for prefix in prefix_filter:
        binary_string = ''.join(format(ord(char), '08b') for char in prefix)

        one_positions = [i for i, bit in enumerate(binary_string) if bit == '1']

        for distance in range(1, max_distance + 1):
            for bit_positions in combinations(one_positions, distance):
                flipped = list(binary_string)
                for pos in bit_positions:
                    flipped[pos] = '0'
                possible_results.add(''.join(flipped))

    possible_results_list = []
    for binary_string in possible_results:
        characters = []
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i + 8]
            if len(byte) == 8:
                char_code = int(byte, 2)
                if 0 <= char_code < 128:
                    characters.append(chr(char_code))
                else:
                    characters.append('?')
        possible_results_list.append(''.join(characters))

    return possible_results_list

