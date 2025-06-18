import PrefixFilter
from collections import defaultdict


def cal_prefixes_double_chars(data, k, d):
    """calculates prefix filter as key-value dictionary with chars d times (redundant)
        param: data []
        param: k (int) number of chars per prefix
        param: d (int) number of times to double char
        return: prefix filter (dictionary)
    """
    prefixes = defaultdict(list)

    for item in data:
        if len(item) >= k:
            prefix = item.split('|')[0][:k]
            prefix_double = ''.join(char * d for char in prefix)
            prefixes[prefix_double].append(item)

    return dict(prefixes)


def restore_prefixes_majority_based(prefixes, k, d):
    """restores corrupted prefixes by choosing the majority char
        param: prefixes []
        param: k (int) number of chars per prefix
        param: d (int) number of times to double char
        return: prefix filter (dictionary)
    """
    true_prefixes = defaultdict(list)
    maybe_prefixes = defaultdict(list)

    for prefix, references in prefixes.items():
        options = [([], True)]
        for i in range(0, len(prefix), d):
            group = prefix[i:i + d]
            if len(set(group)) == 1:
                for option, is_safe in options:
                    option.append(group[0])
            else:
                char_count = {}
                for char in group:
                    if char in char_count:
                        char_count[char] += 1
                    else:
                        char_count[char] = 1

                majority_char, majority_count = max(char_count.items(), key=lambda x: x[1])
                majority_unique = list(char_count.values()).count(majority_count) == 1

                if majority_unique:
                    for option, is_safe in options:
                        option.append(majority_char)
                elif majority_count != 1:
                    # include prefixes with characters that are equally often
                    new_options = []
                    for option, is_safe in options:
                        for char, count in char_count.items():
                            if count == majority_count:
                                new_option = option.copy()
                                new_option.append(char)
                                new_options.append((new_option, False))  # better results with False, could be set to True
                    options = new_options
                else:
                    new_options = []
                    for option, is_safe in options:
                        for char in group:
                            new_option = option.copy()
                            new_option.append(char)
                            new_options.append((new_option, False))  # Mark as Maybe (False)
                    options = new_options

        for option, is_safe in options:
            prefix_str = ''.join(option[:k])
            if prefix_str:
                if is_safe:
                    true_prefixes[prefix_str].extend(references)
                else:
                    maybe_prefixes[prefix_str].extend(references)

    return true_prefixes


def restore_prefixes_conservative(prefixes, k, d):
    """restores corrupted prefixes by choosing only the uncorrupted ones
        param: prefixes []
        param: k (int) number of chars per prefix
        param: d (int) number of times to double char
        return: prefix filter (dictionary)
    """
    true_prefixes = defaultdict(list)
    maybe_prefixes = defaultdict(list)

    for prefix, references in prefixes.items():
        options = [([], True)]
        for i in range(0, len(prefix), d):
            group = prefix[i:i + d]
            if len(set(group)) == 1:
                for option, is_safe in options:
                    option.append(group[0])
                else:
                    new_options = []
                    for option, is_safe in options:
                        for char in group:
                            new_option = option.copy()
                            new_option.append(char)
                            new_options.append((new_option, False))  # Mark as Maybe (False)
                    options = new_options

        for option, is_safe in options:
            prefix_str = ''.join(option[:k])
            if prefix_str:
                if is_safe:
                    true_prefixes[prefix_str].extend(references)
                else:
                    maybe_prefixes[prefix_str].extend(references)
    return true_prefixes


def restore_prefixes_comprehensive(prefixes, k, d):
    """restores corrupted prefixes by calculating all prefixes among the d options for one character
        param: prefixes []
        param: k (int) number of chars per prefix
        param: d (int) number of times to double char
        return: prefix filter (dictionary)
    """
    true_prefixes = defaultdict(list)
    maybe_prefixes = defaultdict(list)

    for prefix, references in prefixes.items():
        options = [([], True)]
        for i in range(0, len(prefix), d):
            group = prefix[i:i + d]
            if len(set(group)) == 1:
                for option, is_safe in options:
                    option.append(group[0])
                else:
                    new_options = []
                    for option, is_safe in options:
                        for char in group:
                            new_option = option.copy()
                            new_option.append(char)
                            new_options.append((new_option, False))  # Mark as Maybe (False)
                    options = new_options

        for option, is_safe in options:
            prefix_str = ''.join(option[:k])
            if prefix_str:
                if is_safe:
                    true_prefixes[prefix_str].extend(references)
                else:
                    maybe_prefixes[prefix_str].extend(references)

    combined_result = {**dict(true_prefixes), **dict(maybe_prefixes)}

    return combined_result


def iteration_optimization(data, error_probabilities, k, b, d):
    """One iteration of corrupting the filter with optimization and counting the confusion matrix for the error probabilities.
        param: Data (list[])
        param: error_probabilities (list[])
        param: k (int), length of prefixes
        param: b (int), number of bits per character
        return: TP list[], TN list[], FP list[], FN list[]
    """

    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []
    inv = []  # has been used to count the number of invalids

    prefixes_old = PrefixFilter.cal_prefix(data, k)
    prefixes = cal_prefixes_double_chars(data, k, d)

    for error_probability in error_probabilities:
        corrupted_prefixes, _ = PrefixFilter.corrupt_filter(prefixes, error_probability, b)
        restored_prefixes = restore_prefixes_majority_based(corrupted_prefixes, k, d)
        TP, TN, FP, FN = PrefixFilter.evaluate_Confusionmatrix(restored_prefixes, prefixes_old, k, b)

        fp_results.append(FP)
        fn_results.append(FN)
        tp_results.append(TP)
        tn_results.append(TN)
        inv.append(0)  #not used anymore

    return tp_results, tn_results, fp_results, fn_results, inv