import os
import pickle

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from utils import avg_and_err


with open("results_gowalla/results_all.pkl", "rb") as f:
    results = pickle.load(f)

# results = {seed: {iter0: [run0,..., run9],...,iter9: [run0,..., run9]}}

ITER = 9
# cm_subsection = reversed(np.linspace(0.3, 1, ITER + 1))
cm_subsection = np.linspace(0.2, 1, ITER + 1)
colors = [cm.GnBu(x) for x in cm_subsection]

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

plt.errorbar(seeds, ews_avg, yerr=ews_err, label="EWS", color=colors[0])

for iter in range(1, ITER - 1):
    runs_avg = []
    runs_err = []
    for seed in seeds:
        runs = results[seed][iter]
        avg, err = avg_and_err(runs)
        runs_avg.append(avg)
        runs_err.append(err)

    plt.errorbar(seeds, runs_avg, yerr=runs_err, label=f"iteration{iter}", color=colors[iter])

plt.errorbar(seeds, irma_avg, yerr=irma_err, label="Irma", color=colors[ITER])

plt.legend()
plt.xlabel("seed size")
plt.ylabel("F1 - score")
plt.grid()
plt.savefig("./figures/svg/fig_gowalla.svg", format='svg', bbox_inches='tight')
plt.savefig("./figures/png/fig_gowalla.png", format='png', bbox_inches='tight')
plt.show()

