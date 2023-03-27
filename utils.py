import os
import pickle
import numpy as np

def load(name, DIR):
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

def avg_and_err(arr):
    avg = sum(arr) / len(arr)
    err = np.std(arr) / np.sqrt(len(arr))
    return avg, err

def combine_runs_to_one(runs):
    max_iter = min([len(run) for run in runs])
    avg_lst = []
    err_lst = []

    for iter in range(max_iter):
        iter_results = [run[iter] for run in runs]
        avg, err = avg_and_err(iter_results)
        avg_lst.append(avg)
        err_lst.append(err)

    return avg_lst, err_lst

def sort_by_first2(a, b):
    temp = sorted(zip(a, b))

    a = [element[0] for element in temp]
    b = [element[1] for element in temp]
    return a, b

