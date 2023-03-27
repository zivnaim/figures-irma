import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from utils import load_full, combine_runs_to_one

plt.rcParams["font.family"] = "Times New Roman"
ITER = 7
results_f1 = load_full("./results_figure5_new/results123/f1.pkl")
results_f1_others = load_full("./results_figure5_new/results456/f1.pkl")

results_weight = load_full("./results_figure5_new/results123/weight.pkl")
results_weight_others = load_full("./results_figure5_new/results456/weight.pkl")

results_precision = load_full("./results_figure5_new/results123/precision.pkl")
results_precision_others = load_full("./results_figure5_new/results456/precision.pkl")

results_msizes = load_full("./results_figure5_new/results123/msizes.pkl")

results_f1 = {params: combine_runs_to_one(runs)[0] for params, runs in results_f1.items()}
# results_f1.update({params: combine_runs_to_one(runs)[0] for params, runs in results_f1_others.items()})

print(sorted(results_f1.keys()))
results_weight = {params: combine_runs_to_one(runs)[0] for params, runs in results_weight.items()}
# results_weight.update({params: combine_runs_to_one(runs)[0] for params, runs in results_weight_others.items()})

results_precision = {params: combine_runs_to_one(runs)[0] for params, runs in results_precision.items()}
# results_precision.update({params: combine_runs_to_one(runs)[0] for params, runs in results_precision_others.items()})

results_msizes = {params: combine_runs_to_one(runs)[0] for params, runs in results_msizes.items()}

def div(arr1, arr2):
    return [arr1[i] / arr2[i] for i in range(min(len(arr1), len(arr2)))]

def get_diff(arr):
    return [arr[i + 1] - arr[i] for i in range(len(arr) - 1)]

def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)

def two_scales(ax1, time, data1, data2, label1="", label2="", i=0,  c1="r", c2="black"):
    ax2 = ax1.twinx()
    ax1.plot(time, data1, color=c1, label=label1)
    ax1.plot([], [], color=c2, label=label2)
    ax2.plot(time, data2, color=c2)

    color_y_axis(ax1, c1)
    color_y_axis(ax2, c2)
    ax2.grid(axis='y')
    if i == 0:
        ax1.legend(loc="lower right")
    return ax1, ax2


s = 15
fig, axes = plt.subplot_mosaic("ABEEFF;CDEEFF", figsize=(15, 3))
axs = [axes["A"], axes["B"], axes["C"], axes["D"], axes["E"], axes["F"]]

# ------ figure 0 -------
# gs = [0, 3, 10, 15]
# gs = [0, 3, 10, 15]
gs = [0, 1, 2, 3]
gs = [3, 2, 0, 1]
for i in range(4):
    p = list(results_f1.keys())[gs[i]]
    print(p)
    time = range(len(results_f1[p]))
    data1 = results_weight[p]
    data2 = results_f1[p]

    two_scales(axs[i], time, data1, data2, "Weight(M)", "F1-score", i)
    axs[i].set_xlabel("Iteration")
    axs[i].set_xticks([0, 2, 4, 6, 8])

# ------ figure 2 -------
# params = list(results_f1.keys())
# for p in params:
#     diff_precision = get_diff(results_precision[p])
#     diff_weight_div_size = get_diff(div(results_weight[p], results_msizes[p]))
#
#     # diff_precision = diff_precision[:5]
#     # diff_weight_div_size = diff_weight_div_size[:5]
#     axs[1].scatter(diff_weight_div_size, diff_precision, color="red", s=1)
#     axs[1].set_xlabel("Difference in |Weight(M)|/|M|")
#     axs[1].set_ylabel("Difference in precision")

# ------ figure 3 -------
params = list(results_f1.keys())
for p in params:
    diff_precision = get_diff(results_precision[p])
    diff_weight_div_size = get_diff(results_weight[p])
    axs[4].scatter(diff_weight_div_size , diff_precision, color="black", s=s)
    axs[4].set_xlabel("Difference in |Weight(M)|")
    axs[4].set_ylabel("Difference in precision")

# ------ figure 4 -------
params = list(results_f1.keys())
for p in params:
    diff_precision = get_diff(results_precision[p])
    x = range(1, 1 + len(diff_precision))
    axs[5].scatter(x, diff_precision, color="black", s=s)
    axs[5].set_xlabel("Iteration")
    axs[5].set_ylabel("Difference in precision")

fig.tight_layout(pad=0.5)
plt.savefig("./figures_new/svg/fig6.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures_new/png/fig6.png", format='png', bbox_inches='tight')
plt.savefig("./figures_new/eps/fig6.eps", format='eps', bbox_inches='tight')
plt.show()
