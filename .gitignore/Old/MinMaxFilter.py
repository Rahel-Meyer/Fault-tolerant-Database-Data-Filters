import random
import numpy as np
import matplotlib.pyplot as plt
import GenerateData


def cal_min_max(data, block_size):
    """ Extracts minimum and maximum value from a block of a table of one column.
        param: Data (list[]), number of entry's per block
        return: list of minimum and maximum values"""

    min_max = []
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        values = [float(item.split('|')[0]) for item in block if item]
        if values:
            min_max.append((min(values), max(values)))
    return min_max


def corrupt_min_max(filter, error_probability):
    """Flips bits in the binary representation of each value with probability p.
    param: filter (list[tuple[float, float]]), error_probability(float): Probability of a bit flip for each bit
    return: list[float]: List of values with corrupted bits"""

    corrupted_filter = []

    for min_val, max_val in filter:
        def corrupt_value(value):
            """Helper function to flip bits in the binary representation of a single value with probability p."""
            int_representation = int(value * 10 ** 6)  # Float to int
            binary = format(int_representation, '032b')
            print(len(binary))

            flipped_binary = ''.join(
                '1' if bit == '0' and random.random() < error_probability else
                '0' if bit == '1' and random.random() < error_probability else bit
                for bit in binary
            )

            return int(flipped_binary, 2) / 10 ** 6  # binary to float

        corrupted_min = corrupt_value(min_val)
        corrupted_max = corrupt_value(max_val)

        corrupted_filter.append((corrupted_min, corrupted_max))

    return corrupted_filter


def evaluate_Confusionmatrix(correct_filter, corrupt_filter, data):
    """Evaluates confusion matrix values for a corrupted filter compared to the correct filter.
      param: correct_filter (list[tuple[float, float]]): List of (min, max) tuples for the correct filter
      param: corrupt_filter (list[tuple[float, float]]): List of (min, max) tuples for the corrupted filter
      param: data (list[float]): List of data entries to check
      return: TP, TN, FP, FN"""
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    if len(correct_filter) != len(corrupt_filter):
        raise ValueError("Both filters must have the same number of (min, max) ranges.")

    for item in data:
        in_correct = False
        in_corrupt = False
        for (correct_min, correct_max), (corrupt_min, corrupt_max) in zip(correct_filter, corrupt_filter):
            if float(correct_min) <= float(item) <= float(correct_max):
                in_correct = True
            if float(corrupt_min) <= float(item) <= float(corrupt_max):
                in_corrupt = True

        if in_correct and in_corrupt:
            true_positives += 1
        elif not in_correct and in_corrupt:
            false_positives += 1
        elif not in_correct and not in_corrupt:
            true_negatives += 1
        elif in_correct and not in_corrupt:
            false_negatives += 1

    return true_positives, true_negatives, false_positives, false_negatives


def plot_Confusionmatrix(data1, data2, blocksize, error_probabilities):
    """Generates plots with Confusionmatrix vs. error probability for different n values.
    param: data (list[str]), error_probabilities (array[float]), n_values (list[int])
    return: None, shows and saves plots
    """
    fp_results = []
    fn_results = []
    tp_results = []
    tn_results = []

    filter = cal_min_max(data1, blocksize)

    for error_probability in error_probabilities:
        corrupted_min_max = corrupt_min_max(filter, error_probability)
        TP, TN, FP, FN = evaluate_Confusionmatrix(corrupted_min_max, filter, data2)

        fp_results.append(FP)
        fn_results.append(FN)
        tp_results.append(TP)
        tn_results.append(TN)

    n = 1000

    plt.figure(figsize=(16, 10))

    plt.subplot(2, 2, 3)
    plt.plot(error_probabilities, fp_results, label=f'result=FP', marker='o')
    # plt.plot(error_probabilities, pred_fp, label=f'prediction={n}', marker='o')
    plt.title('False Positives (FP) vs. Error Probability')
    plt.xlabel('Error Probability')
    plt.ylabel('False Positives (FP)')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(error_probabilities, fn_results, label=f'result=FN', marker='o')
    # plt.plot(error_probabilities, pred_fn, label=f'prediction={n}', marker='o')
    plt.title('False Negatives (FN) vs. Error Probability')
    plt.xlabel('Error Probability')
    plt.ylabel('False Negatives (FN)')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 1)
    plt.plot(error_probabilities, tp_results, label=f'result=TP', marker='o')
    #plt.plot(error_probabilities, pred_tp, label=f'prediction={n}', marker='o')
    plt.title('True Positives (TP) vs. Error Probability')
    plt.xlabel('Error Probability')
    plt.ylabel('True Positives (TP)')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(error_probabilities, tn_results, label=f'result=TN', marker='o')
    # plt.plot(error_probabilities, pred_tn, label=f'prediction={n}', marker='o')
    plt.title('True Negatives (TN) vs. Error Probability')
    plt.xlabel('Error Probability')
    plt.ylabel('True Negatives (TN)')
    plt.legend(loc='best')
    plt.grid(True)

    plt.suptitle(f'FP, FN, TP, and TN vs. Error Probability for blocksize={blocksize}')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


if __name__ == '__main__':
    u = sorted(GenerateData.generate_numeric_data(1000, 2, 9), key=float)
    v = GenerateData.generate_numeric_data(100, 4, 7)
    error_probabilities = np.arange(0.0, 1.0, 0.01)
    plot_Confusionmatrix(u, v, 10, error_probabilities)


### Not used ###

def z_channel_min_max(filter, error_probability):
    """Applies a Z-channel error model to each min/max value in a list of tuples with probability p.
       This means only 1s are flipped to 0s in the binary representation.
       param: filter_data (list[tuple[float, float]]): List of (min, max) tuples
       param: p (float): Probability of flipping a 1 to a 0 for each bit
       return: list[tuple[float, float]]: List of (min, max) tuples with corrupted bits"""

    corrupted_filter = []

    for min_val, max_val in filter:
        def corrupt_value(value):
            """Helper function to flip bits in the binary representation of a single value with probability p."""

            int_representation = int(value * 10 ** 6)
            binary = format(int_representation, '032b')
            flipped_binary = ''.join(
                '0' if bit == '1' and random.random() < error_probability else bit
                for bit in binary
            )

            return int(flipped_binary, 2) / 10 ** 6

        corrupted_min = corrupt_value(min_val)
        corrupted_max = corrupt_value(max_val)
        corrupted_filter.append((corrupted_min, corrupted_max))

    return corrupted_filter


def reverse_z_channel_min_max(filter, error_probability):
    """Applies a reverse-Z-channel error model to each min/max value in a list of tuples with probability p.
       This means only 0s are flipped to 1s in the binary representation.
       param: filter_data (list[tuple[float, float]]): List of (min, max) tuples
       param: p (float): Probability of flipping a 0 to a 1 for each bit
       return: list[tuple[float, float]]: List of (min, max) tuples with corrupted bits"""

    corrupted_filter = []

    for min_val, max_val in filter:
        def corrupt_value(value):
            """Helper function to flip bits in the binary representation of a single value with probability p."""

            int_representation = int(value * 10 ** 6)
            binary = format(int_representation, '032b')
            flipped_binary = ''.join(
                '1' if bit == '0' and random.random() < error_probability else bit
                for bit in binary
            )

            return int(flipped_binary, 2) / 10 ** 6

        corrupted_min = corrupt_value(min_val)
        corrupted_max = corrupt_value(max_val)
        corrupted_filter.append((corrupted_min, corrupted_max))

    return corrupted_filter
