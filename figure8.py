import os
import pickle

import matplotlib.pyplot as plt

from utils import combine_runs_to_one, sort_by_first2

DIR = "./results_figure8"
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


def analyze_info(info):
    info_by_plots = {}
    for (graph_num, overlap, seed, parallel, ews), runs in info.items():
        avg, err = combine_runs_to_one(runs)
        iter_num = -1
        if seed not in [50, 100, 200, 400, 800]:
            continue

        if (graph_num, overlap, parallel, ews) in info_by_plots:
            info_by_plots[(graph_num, overlap, parallel, ews)].append((seed, avg[iter_num], err[iter_num]))
        else:
            info_by_plots[(graph_num, overlap, parallel, ews)] = [(seed, avg[iter_num], err[iter_num])]

    return info_by_plots


def plot_all(info_by_plots, ax):
    colors = {
        1: "blue",
        2: "red",
        3: "green",
        4: "black",
        5: "yellow"
    }
    lines = {
        (False, False): "-",
        (True, False): "--",
        (True, True): ":"
    }
    labels = {
        (False, False): "Irma",
        (True, False): "Irma parallel",
        (True, True): "EWS parallel"
    }

    seeds = set()
    for (graph_num, overlap, parallel, ews), lst in info_by_plots.items():
        if ews:
            continue

        ews_score = info_by_plots[(graph_num, overlap, True, True)]

        lst = sorted(lst)
        ews_score = sorted(ews_score)

        x = [temp[0] for temp in lst]
        # y = [temp[1] - 0 for temp, ews in zip(lst, ews_score)]
        y = [temp[1] - ews[1] for temp, ews in zip(lst, ews_score)]
        err = [temp[2] for temp in lst]
        seeds = seeds.union(set(x))

        label = f"G{graph_num}, s: {overlap}, {labels[(parallel, ews)]}"
        # if graph_num == 1:
        #     if ews:
        #         label = "Parallel EWS"
        #     elif parallel:
        #         label = 'Parallel IRMA'
        #     else:
        #         label = "IRMA"
        # # label += f" G{graph_num}"
        # else:
        #     label = '_nolegend_'

        ax.errorbar(x, y, yerr=err, label=label,
                    color=colors[graph_num], linestyle=lines[(parallel, ews)])
        # ax.errorbar(x, y, yerr=err, label=f"G{graph_num}, s: {overlap}, p: {parallel}",
        #             color=colors[graph_num], linestyle=lines[(parallel, ews)])

    ax.tick_params(axis="x", labelsize=7)
    ax.set_xticks(ticks=list(seeds))
    ax.set_xlabel("Seed")
    ax.grid()
    # ax.legend()


fig, axs = plt.subplots(1, 3, figsize=(15, 3))

precision = load("f1.pkl")
print(precision[(3, 0.5, 400, True, False)])
print(precision[(3, 0.5, 200, True, False)])
precision = analyze_info(precision)
plot_all(precision, axs[0])
axs[0].set_ylabel("F1 - score")

precision = load("precision.pkl")
precision = analyze_info(precision)
plot_all(precision, axs[1])
axs[1].set_ylabel("Precision")

precision = load("recall.pkl")
precision = analyze_info(precision)
plot_all(precision, axs[2])
axs[2].set_ylabel("Recall")

# times = load("times.pkl")
# times = analyze_info(times)
# plot_all(times, axs[3])
# axs[3].set_ylabel("Time")


handles, labels = axs[0].get_legend_handles_labels()
# labels, handles = sort_by_first2(labels, handles)
fig.legend(handles, labels, loc='upper center', ncol=6)

# (graph num, overlap, seed, parallel, ews)

plt.savefig("./figures/svg/fig8.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures/png/fig8.png", format='png', bbox_inches='tight')
plt.savefig("./figures/eps/fig8.eps", format='eps', bbox_inches='tight')
plt.show()
