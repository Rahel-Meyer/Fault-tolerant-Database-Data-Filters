import math
import random


def cal_length(data):
    """saves length from a table of one column.
    param: Data (list[str])
    return: list of different length's"""

    length_set = set(len(item) for item in data if item)
    return sorted(length_set)


def corrupt_length_filter(length_list, error_probability):
    """Corrupts length's based on error probability (flips 1s and 0s).
    Param: length list (list[str]), Error probability (float)
    Return: Corrupted length list, number of bit flips"""

    corrupted_length_list = []
    flip_count = 0

    for length in length_list:
        binary_length = format(length, '08b')
        corrupted_binary = list(binary_length)

        for i in range(len(corrupted_binary)):
            if random.random() < error_probability:
                corrupted_binary[i] = '1' if corrupted_binary[i] == '0' else '0'
                flip_count += 1

        corrupted_length = int(''.join(corrupted_binary), 2)
        corrupted_length_list.append(corrupted_length)

    return corrupted_length_list, flip_count


def evaluate_Confusionmatrix_length(corrupted_filter, correct_filter, data):
    """Evaluates confusion matrix values for a corrupted filter compared to the correct filter.
    Here no indexes are compared so an FP is where the corrupt filter answers yes and the correct filter no.
    param: corrupted and correct Filter for comparison, data to check
    return: TP, TN, FP, FN"""

    data_length = cal_length(data)

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for item in data_length:
        if item in corrupted_filter and item in correct_filter:
            true_positives += 1
        elif item in corrupted_filter and item not in correct_filter:
            false_positives += 1
        elif item not in corrupted_filter and item in correct_filter:
            false_negatives += 1
        elif item not in corrupted_filter and item not in correct_filter:
            true_negatives += 1

    return true_positives, true_negatives, false_positives, false_negatives


def prediction_length_normal(error_probabilities, u, v, max_u, max_v):
    """ Calculates the prediction for the Confusions matrix of the Filter.
    param: error_probabilities (list[])
    param: u (int), length of data u
    param: v (int), length of data v
    return: TP list[], TN list[], FP list[], FN list[]"""
    pred_fp = []
    pred_fn = []
    pred_tp = []
    pred_tn = []

    L_u = round(max_u * math.e ** (-max_u/u))
    L_v = round(max_v * math.e ** (-max_v/v))

    positives = L_u * (L_v / max_u)
    negatives = L_v - positives

    for p in error_probabilities:
        num_flips = (L_u * 8 * p)
        flip = 1-(1-p)**(8)

        # for FP
        flip_negatives_to_v = negatives * flip

        # for FN
        flip_positives_to_negatives = positives * flip

        pred_FP = flip_negatives_to_v
        pred_FN = flip_positives_to_negatives

        pred_TP = positives - flip_positives_to_negatives
        pred_TN = negatives - flip_negatives_to_v

        pred_fp.append(pred_FP/L_v)
        pred_fn.append(pred_FN/L_v)
        pred_tp.append(pred_TP/L_v)
        pred_tn.append(pred_TN/L_v)

    return pred_tp, pred_tn, pred_fp, pred_fn


def length_normal(data, data2, error_probabilities, max_v):
    """Calculates the Confusions matrix of the Filter for the different error probabilities.
    param: Data (list[])
    param: data2 (list[])
    param: error_probabilities (list[])
    param: n_value (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""
    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    length = cal_length(data)
    v = len(data2)
    L_v = round(max_v * math.e ** (-max_v/v))

    for error_probability in error_probabilities:
        corrupted_length, _ = corrupt_length_filter(length, error_probability)
        #without_invalids = PrefixNoInvalids.without_invalids(corrupted_prefixes)
        TP, TN, FP, FN = evaluate_Confusionmatrix_length(corrupted_length, length, data2)

        fp_results.append(FP/L_v)
        fn_results.append(FN/L_v)
        tp_results.append(TP/L_v)
        tn_results.append(TN/L_v)

    return tp_results, tn_results, fp_results, fn_results