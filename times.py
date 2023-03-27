from utils import load_full, combine_runs_to_one
import matplotlib.pyplot as plt

ITER = 9

times = load_full("./results_figure5_new/results123/times.pkl")
times1 = load_full("./results_figure5_new/results456/times.pkl")

times = {params: combine_runs_to_one(runs) for params, runs in times.items()}
times.update({params: combine_runs_to_one(runs) for params, runs in times1.items()})

def plot_figure(results, ax, ylable):
    x = range(ITER)
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xticks(ticks=x)
    for (graph_num, overlap, seed), (lst_avg, lst_err) in results.items():
        ax.errorbar(x, lst_avg[:ITER], yerr=lst_err[:ITER], label=f"G{graph_num}, s: {overlap}, seed: {seed}")

    ax.set_xlabel("Iteration")
    ax.set_ylabel(ylable)
    ax.grid()


print(times)
fig, axs = plt.subplots(1)
plot_figure(times, axs, "times")
axs.set_yscale("log")
plt.show()
