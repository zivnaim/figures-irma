import os
import pickle

import numpy as np
import matplotlib.pyplot as plt


DIR = "./results_figure4"
plt.rcParams["font.family"] = "Times New Roman"


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


def process_results(results: dict):
    new_dict = {}
    for params, arr in results.items():
        arr = [a[0] for a in arr]
        avg = sum(arr) / len(arr)
        error = np.std(arr) / np.sqrt(len(arr))
        new_dict[params] = (avg, error)
    return new_dict


def process_results1(results: dict):
    new_dict = {}
    for params, arr in results.items():
        avg = sum(arr) / len(arr)
        error = np.std(arr) / np.sqrt(len(arr))
        new_dict[params] = (avg, error)
    return new_dict


def plot_figure(results, ax, num, color):
    graphs = [0.5, 0.6, 0.7]
    line_types = ["-", "--", ":"]
    for (s, lt) in zip(graphs, line_types):
        x = []
        y = []
        yerror = []
        for (overlap, seed), (avg, error) in results.items():
            if overlap == s:
                x.append(seed)
                y.append(avg)
                yerror.append(error)

        x, y, yerror = sort_by_first(x, y, yerror)

        ax.tick_params(axis="x", labelsize=7)
        ax.set_xticks(ticks=x)
        ax.errorbar(x, y, yerr=yerror, label=f"G{num}, s: {s}", linestyle=lt, color=color)

    ax.set_xlabel("Seed size")
    ax.grid()
    ax.legend()


def plot_graphs(ax, stats_name, label):
    ax.set_ylabel(label)
    temp = process_results(g2_results[stats_name])
    plot_figure(temp, ax, 2, COLOR2)

    temp = process_results1(g3_results[stats_name])
    plot_figure(temp, ax, 3, COLOR3)
    ax.grid()


COLOR2 = "black"
# COLOR3 = "#66b2ff"
COLOR3 = "blue"

ews_results = load("fig4_ews_results.pkl")
print(ews_results)

g2_results = ews_results[2]
g3_results = ews_results[3]

fig, axs = plt.subplots(1, 4, figsize=(18, 3))

plot_graphs(axs[0], "f1", "F1 - score")
plot_graphs(axs[1], "precision", "Precision")
plot_graphs(axs[2], "recall", "Recall")

# ----- The forth graph - parallel ews -----
parallel_results = load("./results_ews/parallel23_f1.pkl")
parallel_results = process_results1(parallel_results)
parallel_results2 = \
    {(overlap, seed): res for (graph_num, overlap, seed), res in parallel_results.items() if graph_num == 2}
parallel_results3 = \
    {(overlap, seed): res for (graph_num, overlap, seed), res in parallel_results.items() if graph_num == 3}

plot_figure(parallel_results2, axs[3], 2, COLOR2)
plot_figure(parallel_results3, axs[3], 3, COLOR3)
axs[3].set_ylabel("F1 - score, parallel version")
axs[3].grid()

plt.savefig("./figures/svg/fig4.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures/png/fig4.png", format='png', bbox_inches='tight')
plt.savefig("./figures/eps/fig4.eps", format='eps', bbox_inches='tight')
plt.show()
