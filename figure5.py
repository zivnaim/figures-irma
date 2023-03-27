import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from utils import load_full, combine_runs_to_one

plt.rcParams["font.family"] = "Times New Roman"
ITER = 7
all_results = load_full("./results_figure5_new/results123/f1.pkl")

g1_f1_results = {seed: arr for (graph, s, seed), arr in all_results.items() if graph == 1}
g2_f1_results = {seed: arr for (graph, s, seed), arr in all_results.items() if graph == 2}
g3_f1_results = {seed: arr for (graph, s, seed), arr in all_results.items() if graph == 3}

cm_subsection = reversed(np.linspace(0, 1, ITER + 1))
colors = [cm.winter(x) for x in cm_subsection]

def g1_to_heatmap(results):
    new = {}
    for seed, values in results.items():
        avg_values = [calc_avg([val[iter_num] for val in values]) for iter_num in range(9)]
        new[(1, 0.6, seed)] = avg_values

    return new

def build_dif(results: dict):
    # here we should sort by keys - graphs + seeds
    graphs = sorted(list(results.keys()), key=lambda x: x[0]*100000+x[2])
    iterations = []
    for iter in range(8):
        iter_diffs = []
        last_graph = 1
        for graph in graphs:
            if graph[2] not in [25, 50, 100, 200, 400, 800, 1600]:
                continue

            print(graph)

            if last_graph != graph[0]:
                last_graph = graph[0]
                iter_diffs.append(11)

            running = results[graph]
            # dif = max((running[iter + 1] - running[iter]), 0)
            dif = (running[iter + 1] - running[iter])
            iter_diffs.append(dif)

        iterations.append(iter_diffs)
    return iterations, graphs


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # print(data)
    # print(data.shape)
    new_img = data

    # cmap = matplotlib.cm.GnBu.reversed()
    cmap = matplotlib.cm.Blues
    # cmap = matplotlib.cm.binary
    im = ax.imshow(new_img, cmap=cmap, vmin=data.min(), vmax=data.max(), aspect='auto')

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    # cbar = None

    # Show all ticks and label them with the respective list entries.
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=False,
                   axis='x',  # changes apply to the x-axis
                   which='both',
                   labeltop=False, labelbottom=False)

    return im, cbar


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


def calc_avg(arr):
    return sum(arr) / len(arr)


def calc_error(arr):
    return np.std(arr) / np.sqrt(len(arr))


def plot_figures(results: dict, ax):
    seeds = list(results.keys())
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xticks(ticks=[s for s in seeds if s >= 100])
    ax.grid()

    for iter_num in range(ITER):
        x = []
        y = []
        err = []
        for seed, seed_results in results.items():
            if seed < 100:
                continue

            seed_iter_results = [running[iter_num] for running in seed_results]
            avg = calc_avg(seed_iter_results)
            error = calc_error(seed_iter_results)

            x.append(seed)
            y.append(avg)
            err.append(error)

        x, y, err = sort_by_first(x, y, err)
        ax.errorbar(x, y, yerr=err, label=f"iteration {iter_num}", color=colors[iter_num], capsize=4, capthick=1) #, color=colors[iter_num])

    ax.set_xlabel("Seed size")
    ax.set_ylabel("F1-score")
    ax.legend()


def plot_heatmap(iterations, keys, ax):
    # keys = (graph, overlap, seed)

    heatmap(np.array(iterations), np.arange(1, 9), keys, ax=ax)
    ax.set_ylabel("Iteration")
    # ax.set_title("Delta in F1-score")
    ax.set_title(r'$\Delta$ F1-score')



fig, axs = plt.subplots(1, 3, figsize=(15, 3))
# fig, axs = plt.subplots(1, 4, figsize=(18, 3))

axs[0].set_title("G2")
plot_figures(g2_f1_results, axs[0])

axs[1].set_title("G3")
plot_figures(g3_f1_results, axs[1])

# heat_f1 = g1_to_heatmap(g2_f1_results)
heat_f1 = load_full("./results_figure5_new/results123/f1.pkl") | load_full("./results_figure5_new/results456/f1.pkl")
heat_f1 = {params: combine_runs_to_one(runs)[0] for params, runs in heat_f1.items()}
iterations, keys = build_dif(heat_f1)
plot_heatmap(iterations, keys, axs[2])

# heat_f1 = load_full("./results_heatmap/times.pkl")
# heat_f1 = {params: combine_runs_to_one(runs)[0] for params, runs in heat_f1.items()}
# iterations, keys = build_dif(heat_f1)
# plot_heatmap(iterations, keys, axs[3])
#
# heat_f1 = load_full("./results_heatmap/precision.pkl")
# heat_f1 = {params: combine_runs_to_one(runs)[0] for params, runs in heat_f1.items()}
# iterations, keys = build_dif(heat_f1)
# plot_heatmap(iterations, keys, axs[4])

plt.savefig("./figures_new/svg/fig5.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures_new/png/fig5.png", format='png', bbox_inches='tight', dpi=1200)
plt.savefig("./figures_new/eps/fig5.eps", format='eps', bbox_inches='tight')
plt.show()
