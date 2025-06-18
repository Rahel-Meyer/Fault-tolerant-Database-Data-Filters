import string
import math


def without_invalids(prefix_filter):
    """Deletes all prefixes who`s characters aren`t all printable.
    param: prefix filter with invalids, list[]
    return: prefix filter without invalids, list[]"""
    valid_prefixes = []
    for prefix in prefix_filter:
        if all(char in string.printable for char in prefix):
            valid_prefixes.append(prefix)
    return valid_prefixes


def no_invalids(data, data2, error_probabilities, n_value):
    """Calculates the Confusions matrix of the Filter without invalids for the different error probabilities.
    param: Data (list[])
    param: data2 (list[])
    param: error_probabilities (list[])
    param: n_value (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""

    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    prefixes = PrefixFilter.prefix_set(data, n_value)
    n = n_value
    num_characters = 100
    M = num_characters ** n
    u = len(data)
    P_U = M * (1 - (1 - 1 / M) ** u)

    for error_probability in error_probabilities:
        printable_prefixes = without_invalids(prefixes)
        corrupted_prefixes, _ = PrefixFilter.corrupt_set(printable_prefixes, error_probability)
        TP, TN, FP, FN = PrefixFilter.evaluate_Confusionmatrix_set(corrupted_prefixes, prefixes, data2, n_value)

        fp_results.append(FP / P_U)
        fn_results.append(FN / P_U)
        tp_results.append(TP / P_U)
        tn_results.append(TN / P_U)

    return tp_results, tn_results, fp_results, fn_results


def prediction_no_invalids(error_probabilities, u, v, n):
    """ Calculates the prediction for the Confusions matrix of the Filter without invalids.
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