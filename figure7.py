import os
import pickle

import numpy as np
import matplotlib.pyplot as plt


DIR = "./results_figure7/new_results"
ITER = 10
plt.rcParams["font.family"] = "Times New Roman"

def build_time_from_beginning(arr):
    new_times = []
    time_sum = 0
    for t in arr:
        time_sum += t
        new_times.append(time_sum)
    return new_times

def load(name):
    with open(os.path.join(DIR, name), "rb") as f:
        return pickle.load(f)


def load_full(name):
    with open(name, "rb") as f:
        return pickle.load(f)


def sort_by_first(a, b, c):
    temp = sorted(zip(a, b, c))

    a = [element[0] for element in temp]
    b = [element[1] for element in temp]
    c = [element[2] for element in temp]
    return a, b, c

def sort_by_first2(a, b):
    temp = sorted(zip(a, b))

    a = [element[0] for element in temp]
    b = [element[1] for element in temp]
    return a, b

def process_results(results: dict):
    new_dict = {}
    for params, arr in results.items():
        lst_avg = []
        lst_err = []
        for iter in range(ITER):
            iter_arr = [a[iter] for a in arr]
            avg = sum(iter_arr) / len(iter_arr)
            error = np.std(iter_arr) / np.sqrt(len(iter_arr))
            lst_avg.append(avg)
            lst_err.append(error)
        new_dict[params] = (lst_avg, lst_err)
    return new_dict


def plot_figure(results, ax, ylable):
    x = range(ITER)
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xticks(ticks=x)
    for (graph_num, overlap, seed), (lst_avg, lst_err) in results.items():
        ax.errorbar(x, lst_avg, yerr=lst_err, label=f"G{graph_num}, s: {overlap}, seed: {seed}")

    ax.set_xlabel("Iteration")
    ax.set_ylabel(ylable)
    ax.grid()
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
    #           ncol=3, fancybox=True, shadow=True)
    # ax.legend(ncol=3)


COLOR2 = "#66cc00"
# COLOR3 = "#66b2ff"
COLOR3 = "red"

precision = load("precision.pkl")
recall = load("recall.pkl")
f1 = load("f1.pkl")
times = load("times.pkl")

fig, axs = plt.subplots(1, 4, figsize=(19, 3))

f1 = process_results(f1)
plot_figure(f1, axs[0], "F1 - score")

precision = process_results(precision)
plot_figure(precision, axs[1], "Precision")

recall = process_results(recall)
plot_figure(recall, axs[2], "Recall")

for params, arrs in times.items():
    times[params] = [build_time_from_beginning(arr) for arr in arrs]

print(times)
times = process_results(times)
plot_figure(times, axs[3], "Time (seconds)")
axs[3].set_yscale("log")


handles, labels = axs[0].get_legend_handles_labels()
labels, handles = sort_by_first2(labels, handles)
fig.legend(handles, labels, loc='upper center', ncol=6)

plt.savefig("./figures/svg/fig7.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures/png/fig7.png", format='png', bbox_inches='tight')
plt.savefig("./figures/eps/fig7.eps", format='eps', bbox_inches='tight')
plt.show()
