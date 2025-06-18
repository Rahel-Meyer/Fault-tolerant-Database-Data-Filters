import matplotlib.pyplot as plt
import GenerateData
import numpy as np
import math
from Old import PrefixNoInvalids
import Tests


def cal_prefix_set(data, n):
    """ Calculates prefixes from a table of one column.
    param: Data (list[]), number of characters per prefix n
    return: list of different Prefixes"""

    prefixes = set()
    for item in data:
        if item:
            prefix = item.split('|')[0][:n]
            prefixes.add(prefix)

    return list(prefixes)


def corrupt_set(prefix_list, error_probability):
    """Corrupts prefixes based on error probability (flips 1s and 0s).
    Param: Prefix list (list[str]), Error probability (float)
    Return: Corrupted prefix list, number of bit flips"""

    corrupted_prefix_list = []

    for prefix in prefix_list:
        corrupted_prefix = Tests.corrupt_prefix(prefix, error_probability)
        corrupted_prefix_list.append(corrupted_prefix)

    return corrupted_prefix_list


def evaluate_Confusionmatrix_set(corrupted_filter, correct_filter, data, n):
    """Evaluates confusion matrix values for a corrupted filter compared to the correct filter.
    Here no indexes are compared so an FP is where the corrupt filter answers yes and the correct filter no.
    param: corrupted and correct Filter for comparison, data to check, n=size of Prefixes
    return: TP, TN, FP, FN"""

    data_prefixes = {item.split('|')[0][:n] for item in data if item}

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for item in data_prefixes:
        if item in corrupted_filter and item in correct_filter:
            true_positives += 1
        elif item in corrupted_filter and item not in correct_filter:
            false_positives += 1
        elif item not in corrupted_filter and item in correct_filter:
            false_negatives += 1
        elif item not in corrupted_filter and item not in correct_filter:
            true_negatives += 1

    return true_positives, true_negatives, false_positives, false_negatives


def prediction_set(error_probabilities, u, v, n):
    """ Calculates the prediction for the Confusions matrix of the set-Filter.
    param: error_probabilities (list[])
    param: u (int), length of data u
    param: v (int), length of data v
    param: n (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""

    pred_fp = []
    pred_fn = []
    pred_tp = []
    pred_tn = []

    num_characters = 256
    M = num_characters ** n
    P_U = M * (1 - (1 - 1 / M) ** u)  #929, 920, 922, 930
    P_V = M * (1 - (1 - 1 / M) ** v)
    u_union_v = M * (1 - (1 - 1 / M) ** (u + v))
    u_intersect_v = P_U + P_V - u_union_v
    positives = u_intersect_v #46, 47
    negative_v = P_V - u_intersect_v #920, 933
    negative_u = P_U - u_intersect_v
    f = (u/v)

    for p in error_probabilities:
        #invalids = P_U_old * (1-(1-p*(156/256)*((math.log(100,2))/8) * (1-(100/256)))**(n*math.log(100,2)))
        #positive_invalids = positives_old * (1-(1-p*(156/256)*((math.log(100,2))/8) * (1-(100/256)))**(n*math.log(100,2)))
        #negative_invalids = negative_u_old * (1-(1-p*(156/256)*((math.log(100,2))/8) * (1-(100/256)))**(n*math.log(100,2)))
        #P_U = P_U_old - invalids

        #positives_new = positives_old - positive_invalids
        #negative_u_new = negative_u_old - negative_invalids

        num_flips = (P_U * 8 * n * p)
        flip = 1-(1-p)**(n*8)


        # for FP
        flip_negatives_to_v = negative_u * (negative_v/M) * flip

        # for FN
        flip_positives_to_negatives = positives * ((M - P_V) / M) * flip

        pred_FP = flip_negatives_to_v
        pred_FN = flip_positives_to_negatives

        pred_TP = positives - flip_positives_to_negatives
        pred_TN = negative_v - flip_negatives_to_v

        pred_fp.append(pred_FP)
        pred_fn.append(pred_FN)
        pred_tp.append(pred_TP)
        pred_tn.append(pred_TN)

    return pred_tp, pred_tn, pred_fp, pred_fn


def set_iteration(data, data2, error_probabilities, n_value):
    """Calculates the Confusions matrix of the set-Filter for the different error probabilities.
    param: Data (list[])
    param: data2 (list[])
    param: error_probabilities (list[])
    param: n_value (int), length of prefixes
    return: TP list[], TN list[], FP list[], FN list[]"""

    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    prefixes = cal_prefix_set(data, n_value)
    n = n_value
    num_characters = 100
    M = num_characters ** n
    v = len(data2)
    P_V = M * (1 - (1 - 1 / M) ** v)

    for error_probability in error_probabilities:
        corrupted_prefixes = corrupt_set(prefixes, error_probability)
        TP, TN, FP, FN = evaluate_Confusionmatrix_set(corrupted_prefixes, prefixes, data2, n_value)

        fp_results.append(FP)
        fn_results.append(FN)
        tp_results.append(TP)
        tn_results.append(TN)

    return tp_results, tn_results, fp_results, fn_results

#if __name__ == '__main__':
def invalids():
    error_probabilities = np.arange(0.0, 1.0, 0.05)
    # error_probabilities = np.array([10 ** -5, 10 ** -4, 10 ** -3, 10 ** -2])
    # error_probabilities = np.linspace(0.00001, 0.01, 5)
    n = 2
    u = 5000
    v = 5000
    d1 = 2
    d2 = 2
    num_iterations = 1

    data = GenerateData.generate_ascii_data(8000, 5, 10)
    prefixes = cal_prefix_set(data, n)
    invalids = []
    pred = []
    for p in error_probabilities:
        corrupted, _ = corrupt_set(prefixes, p)
        valid = PrefixNoInvalids.without_invalids(corrupted)
        invalid = len(prefixes) - len(valid)
        invalids.append(invalid)
        #pred.append(len(prefixes) *(1-(1-p*(156/256) * (1-(100/256)))**(n*math.log(100,2)))) #*((math.log(100,2))/8)
        #pred.append(len(prefixes) * (1 - (1 - p * (156/256) * ((math.log(100,2))/8) * (1-(100/256))) ** (n * 8)))
        pred.append(len(prefixes) * (1 - (1 - p * (156/256) * (1-(100/256))*((math.log(156,2))/8))**(n*math.log(156,2))))

    plt.figure(figsize=(16, 10))

    plt.plot(error_probabilities, invalids, label='invalids', marker='o')
    plt.plot(error_probabilities, pred, label='prediction', marker='o')

    plt.title('Number of invalid Prefixes')
    # plt.title(f'Confusion Matrix vs. Error Probability for n={n}, |U|={u} and |V|={v}', fontsize=18)
    plt.xlabel('Error Probability', fontsize=14)
    plt.ylabel('Counts', fontsize=14)

    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
