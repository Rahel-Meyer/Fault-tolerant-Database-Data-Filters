import numpy as np
from matplotlib import pyplot as plt
import GenerateData
import Prediction
import PrefixFilter
import PrefixRedundancy


def cal_stats(TP, TN, FP, FN):
    """Calculates precision, recall and F1 score statistics.
        param: TP [], TN[], FP[], FN[]
        return: precision, recall, f1_score
    """
    recall = []
    precision = []
    f1_score = []

    for tp, tn, fp, fn in zip(TP, TN, FP, FN):
        re = tp / (tp + fn)
        pre = tp / (tp + fp)
        recall.append(re)
        precision.append(pre)
        f1_score.append(2 * ((pre * re) / (pre + re)))

    return recall, precision, f1_score


def run_experiment(num_iterations, error_probabilities, n, k, b, d, opti):
    """Runs the experiment multiple times. For each iteration new data is generated.
    Then the confusion matrix for this data is calculated.
    Statistic measures are calculated over all these confusion matrices.
        param: num_iterations (int)
        param: error_probabilities ([float])
        param: n (int), length of data
        param: k (int), number of characters per prefix
        param: b (int), number of bits per character
        param: d (int), number of duplicates per character
        param: opti (bool), whether to optimize the filter
        return: stats_per_error_prob{}{}{}"""
    stats_per_error_prob = {
        "mean": {},
        "std": {},
        "median": {}
    }

    tp_lists = {p: [] for p in error_probabilities}
    tn_lists = {p: [] for p in error_probabilities}
    fp_lists = {p: [] for p in error_probabilities}
    fn_lists = {p: [] for p in error_probabilities}
    invalid_lists = {p: [] for p in error_probabilities}

    for _ in range(num_iterations):
        if opti:  # filter with optimization
            data = GenerateData.generate_ascii_data(n, 5, 5)
            TP, TN, FP, FN, invalids = PrefixRedundancy.iteration_optimization(data, error_probabilities, k, b, d)
        else:  # filter without optimization
            if b == 5:  # realistic input
                data = GenerateData.generate_text_from_ascii_freq(n, 3, 10, 'ascii_freq.json')
                TP, TN, FP, FN, invalids = PrefixFilter.iteration_filter(data, error_probabilities, k, b)
            else:  # uniform input
                data = GenerateData.generate_ascii_data(n, 5, 5)
                TP, TN, FP, FN, invalids = PrefixFilter.iteration_filter(data, error_probabilities, k, b)

        for i, p in enumerate(error_probabilities):
            tp_lists[p].append(TP[i])
            tn_lists[p].append(TN[i])
            fp_lists[p].append(FP[i])
            fn_lists[p].append(FN[i])
            invalid_lists[p].append(invalids[i])

    for p in error_probabilities:
        tp_array = np.array(tp_lists[p])
        tn_array = np.array(tn_lists[p])
        fp_array = np.array(fp_lists[p])
        fn_array = np.array(fn_lists[p])
        invalid_array = np.array(invalid_lists[p])

        stats_per_error_prob["mean"][p] = (
            np.mean(tp_array), np.mean(tn_array), np.mean(fp_array), np.mean(fn_array), np.mean(invalid_array)
        )
        stats_per_error_prob["std"][p] = (
            np.std(tp_array), np.std(tn_array), np.std(fp_array), np.std(fn_array), np.std(invalid_array)
        )
        stats_per_error_prob["median"][p] = (
            np.median(tp_array), np.median(tn_array), np.median(fp_array), np.median(fn_array), np.median(invalid_array)
        )

    return stats_per_error_prob


def see_stats(n, k, b, d, num_iterations, opti):
    """ Creates three graphs as output
        param: n (int), length of data
        param: k (int), number of characters per prefix
        param: b (int), number of bits per character
        param: d (int), number of duplicates per character
        param: num_iterations (int)
        param: opti (bool), whether to optimize the filter
    """
    error_probabilities = np.arange(0.0, 0.55, 0.05)

    stats_uni = run_experiment(num_iterations, error_probabilities, n, k, b, d, opti)
    TP = [stats_uni["mean"][p][0] for p in stats_uni["mean"]]
    TN = [stats_uni["mean"][p][1] for p in stats_uni["mean"]]
    FP = [stats_uni["mean"][p][2] for p in stats_uni["mean"]]
    FN = [stats_uni["mean"][p][3] for p in stats_uni["mean"]]
    recall_uni, precision_uni, f1_score_uni = cal_stats(TP, TN, FP, FN)

    plt.figure(figsize=(16, 10))
    plt.subplot(3, 1, 1)
    plt.plot(error_probabilities, recall_uni, label=f'Recall', color='blue', marker='o')
    plt.xlabel('Error Probability')
    plt.ylabel(r' Recall / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(error_probabilities, precision_uni, label=f'Precision', color='blue', marker='o')
    plt.xlabel('Error Probability')
    plt.ylabel(r' Precision / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(error_probabilities, f1_score_uni, label=f'F1-score', color='blue', marker='o')
    plt.xlabel('Error Probability')
    plt.ylabel(r' F1-score / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.suptitle(f'Metrics vs. Error Probability for k={k}, n={n}, and {num_iterations} iterations')
    plt.show()


def see_confusion_matrix(num_iterations, n, k, b, d, opti):
    """ Creates confusion matrix graph as output
        param: n (int), length of data
        param: k (int), number of characters per prefix
        param: b (int), number of bits per character
        param: d (int), number of duplicates per character
        param: num_iterations (int)
        param: opti (bool), whether to optimize the filter
    """
    error_probabilities = np.arange(0.0, 1.05, 0.05)

    stats_uni = run_experiment(num_iterations, error_probabilities, n, k, b, d, opti)
    if b == 5:
        TPr, TNr, FPr, FNr = Prediction.pred_real_distr(error_probabilities, n, k, b)
    else:
        TPr, TNr, FPr, FNr = Prediction.pred_uni_distr(error_probabilities, n, k, b)

    TP = [stats_uni["mean"][p][0] for p in stats_uni["mean"]]
    TN = [stats_uni["mean"][p][1] for p in stats_uni["mean"]]
    FP = [stats_uni["mean"][p][2] for p in stats_uni["mean"]]
    FN = [stats_uni["mean"][p][3] for p in stats_uni["mean"]]

    plt.figure(figsize=(16, 10))

    plt.subplot(2, 2, 3)
    plt.plot(error_probabilities, FP, label=f'Simulation', marker='o')
    plt.plot(error_probabilities, FPr, label=f'Prediction', marker='o')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Error Probability')
    plt.ylabel(r'Mean FP / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(error_probabilities, FN, label=f'Simulation', marker='o')
    plt.plot(error_probabilities, FNr, label=f'Prediction', marker='o')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Error Probability')
    plt.ylabel(r'Mean FN / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 1)
    plt.plot(error_probabilities, TP, label=f'Simulation', marker='o')
    plt.plot(error_probabilities, TPr, label=f'Prediction', marker='o')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Error Probability')
    plt.ylabel(r'Mean TP / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(error_probabilities, TN, label=f'Simulation', marker='o')
    plt.plot(error_probabilities, TNr, label=f'Prediction', marker='o')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.xlabel('Error Probability')
    plt.ylabel(r'Mean TN / $\Omega$')
    plt.legend(loc='best')
    plt.grid(True)

    plt.suptitle(f'Confusion Matrix vs. Error Probability for k={k}, n={n}, d={d}, and {num_iterations} iterations')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
