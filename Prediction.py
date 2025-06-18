import json
import math
from itertools import product


def pred_uni_distr(error_probabilities, n, k, b):
    """ Calculates the prediction for the Confusions matrix with a uniform distribution among the characters
        param: error_probabilities (list[])
        param: n (int), length of data
        param: k (int), number of characters per prefix
        param: b (int), number of bits per character
        return: TP list[], TN list[], FP list[], FN list[]"""

    pred_fp = []
    pred_fn = []
    pred_tp = []
    pred_tn = []

    num_characters = 2 ** b
    M = num_characters ** k
    m = M * (1 - (1 - 1 / M) ** n)

    for p in error_probabilities:
        bf = m * b * k * p  # number of bit flips
        flip = (1 - (1 - p) ** (b * k))
        flips = m * flip
        no_flips = m - flips
        msecond = (M * (1 - (1 - 1 / M) ** flips))

        coll_to_no_flips = msecond * no_flips / M
        FP2m = msecond * m / M
        dfgh = msecond * no_flips / M

        TP = no_flips - coll_to_no_flips  # unveraendert - getroffen
        FP = msecond  # flip - coll - treffer_auf_alten
        FN = flips - FP2m + dfgh  # flips - treffer_auf_m + treffer_auf_volle_m
        TN = M - TP - FN - FP

        pred_fp.append(FP/M)
        pred_fn.append(FN/M)
        pred_tp.append(TP/M)
        pred_tn.append(TN/M)

    return pred_tp, pred_tn, pred_fp, pred_fn


def pred_real_distr(error_probabilities, n, k, b):
    """ Calculates the prediction for the Confusions matrix with realistic frequencies among the characters
        param: error_probabilities (list[])
        param: n (int), length of data
        param: k (int), number of characters per prefix
        param: b (int), number of bits per character
        return: TP list[], TN list[], FP list[], FN list[]"""

    pred_fp = []
    pred_fn = []
    pred_tp = []
    pred_tn = []

    num_characters = 2 ** b
    M = num_characters ** k
    m = pref_filter_size(n, k)

    for p in error_probabilities:
        bf = m * b * k * p  # number of bit flips
        flip = (1 - (1 - p) ** (b * k))
        flips = m * flip
        no_flips = m - flips

        flip_prob = {
            "1": math.comb(5, 1) * (p ** 1) * ((1 - p) ** (5 - 1)),
            "2": math.comb(5, 2) * (p ** 2) * ((1 - p) ** (5 - 2)),
            "3": math.comb(5, 3) * (p ** 3) * ((1 - p) ** (5 - 3)),
            "4": math.comb(5, 4) * (p ** 4) * ((1 - p) ** (5 - 4)),
            "5": math.comb(5, 5) * (p ** 5)
        }

        a = range(1, 6)
        invalids = m * sum(flip_prob[str(g)]for g in a) * (6/32) * k
        valids = flips - invalids
        i_coll = 36*(1-(1-(1/36))**invalids)
        v_coll = (676 * (1 - (1 - 1 / 676) ** valids))
        msecond = (M * (1 - (1 - 1 / M) ** flips))
        coll_to_no_flipstp = msecond * no_flips / M
        coll_to_no_flipsfp = v_coll * no_flips / M
        outside_m = invalids + v_coll * (M - m) / M

        TP = no_flips - coll_to_no_flipstp  # unveraendert - getroffen
        FP = msecond # flip - coll - treffer_auf_alten
        FN = outside_m + coll_to_no_flipsfp  # flips_ausserhalb + flips auf unveraendert
        TN = M - TP - FN - FP

        pred_fp.append(FP/M)
        pred_fn.append(FN/M)
        pred_tp.append(TP/M)
        pred_tn.append(TN/M)

    return pred_tp, pred_tn, pred_fp, pred_fn


def pref_filter_size(n, k):
    """ Calculates the predicted size of the prefix filter with a realistic distribution among the characters
        param: error_probabilities (list[])
        param: n (int), length of data
        param: k (int), number of characters per prefix
        return: m (float), predicted number of different prefixes"""
    with open('ascii_freq.json', 'r') as f:
        data = json.load(f)

    ascii_prob_map = {entry["ascii"]: entry["frequency"] for entry in data.values()}
    ascii_codes = list(ascii_prob_map.keys())

    prob_list = []

    for prefix in product(ascii_codes, repeat=k):
        p = 1.0
        for code in prefix:
            p *= ascii_prob_map[code]
        prob_list.append(p)
    m = sum(1 - (1 - p) ** n for p in prob_list)
    return m
