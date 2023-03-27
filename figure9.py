import os
import pickle

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from utils import avg_and_err, load_full, combine_runs_to_one

with open("results_gowalla/results_all.pkl", "rb") as f:
    results = pickle.load(f)

# results = {seed: {iter0: [run0,..., run9],...,iter9: [run0,..., run9]}}

ITER = 9
# cm_subsection = reversed(np.linspace(0.3, 1, ITER + 1))
# cm_subsection = np.linspace(0.2, 1, ITER + 1)
# colors = [cm.GnBu(x) for x in cm_subsection]

cm_subsection = reversed(np.linspace(0.15, 0.6, ITER + 1))
colors = [cm.jet(x) for x in cm_subsection]

print(results)

seeds = [25, 50, 100, 150, 200]

ews_err = []
ews_avg = []

irma_err = []
irma_avg = []

for seed in seeds:
    ews_seed = results[seed][0]
    irma_seed = results[seed][9]

    avg, err = avg_and_err(ews_seed)
    ews_avg.append(avg)
    ews_err.append(err)

    avg, err = avg_and_err(irma_seed)
    irma_avg.append(avg)
    irma_err.append(err)

fig, axs = plt.subplots(1, 1, figsize=(5, 4))
axs = [axs]

axs[0].errorbar(seeds, ews_avg, yerr=ews_err, label="EWS", color=colors[0])

for iter in range(1, ITER - 1):
    runs_avg = []
    runs_err = []
    for seed in seeds:
        runs = results[seed][iter]
        avg, err = avg_and_err(runs)
        runs_avg.append(avg)
        runs_err.append(err)

    axs[0].errorbar(seeds, runs_avg, yerr=runs_err, label=f"iteration{iter}", color=colors[iter])

axs[0].errorbar(seeds, irma_avg, yerr=irma_err, label="Irma", color=colors[ITER])

axs[0].legend()
axs[0].set_xlabel("seed size")
axs[0].set_ylabel("F1 - score")
axs[0].grid()
#
# # -------------------------------
# def plot_irma_deg(f1_scores, ax, label):
#     new_dict = {}
#     for i, runs in f1_scores.items():
#         avg, err = avg_and_err(runs)
#         new_dict[i] = (avg, err)
#
#     weeks = [i for i in range(9)]
#     deg2_vals = [new_dict[i][0] for i in weeks]
#     deg2_errs = [new_dict[i][1] for i in weeks]
#
#     ax.errorbar(weeks, deg2_vals, yerr=deg2_errs, label=label)
#
#
# pre_deg2 = load_full("./results_figure9/oregon_precision_deg2.pkl")
# pre_deg3 = load_full("./results_figure9/oregon_precision_deg3.pkl")
# # f1_deg4 = load_full("./results_figure9/oregon_f1_deg4.pkl")
# # f1_deg5 = load_full("./results_figure9/oregon_f1_deg5.pkl")
#
# plot_irma_deg(pre_deg2, axs[1], "Irma - deg >= 2")
# plot_irma_deg(pre_deg3, axs[1], "Irma - deg >= 3")
# # plot_irma_deg(f1_deg4, axs[1])
# # plot_irma_deg(f1_deg5, axs[1])
#
# DDM = [0.63, 0.37, 0.34, 0.3, 0.28, 0.28, 0.26, 0.245, 0.245]
# PLD = [1, 0.73, 0.695, 0.65, 0.62, 0.6, 0.583, 0.554, 0.45]
#
# weeks = list(range(9))
# axs[1].errorbar(weeks, DDM, label="DDM (2016)")
# axs[1].errorbar(weeks, PLD, label="PLD (2021)")
#
# axs[1].legend()
# axs[1].set_xlabel("Difference in weeks")
# axs[1].set_ylabel("Precision")
# axs[1].grid()

plt.savefig("./figures/svg/fig9.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures/png/fig9.png", format='png', bbox_inches='tight')
plt.savefig("./figures/eps/fig9.eps", format='eps', bbox_inches='tight')
plt.show()

