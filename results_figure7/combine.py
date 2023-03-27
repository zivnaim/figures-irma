import os
import pickle

dirs = ["./original_graphs", "./other_graphs"]
names = ["count.pkl", "f1.pkl", "precision.pkl", "recall.pkl"]

for name in names:
    new_d = {}
    for dir in dirs:
        path = os.path.join(dir, name)
        with open(path, "rb") as f:
            d = pickle.load(f)
            new_d.update(d)

    with open(name, "wb") as f:
        pickle.dump(new_d, f)


# First iteration (EWS) time was tested separately from the other iterations times.


name = "times.pkl"
new_d = {}
for dir in dirs:
    path1 = os.path.join("./times_ews", name)
    path2 = os.path.join(dir, name)
    with open(path1, "rb") as f:
        d1 = pickle.load(f)

    with open(path2, "rb") as f:
        d2 = pickle.load(f)


    for key in d2:
        ts = [lst1 + lst2 for lst1, lst2 in zip(d1[key], d2[key])]
        new_d[key] = ts

with open(name, "wb") as f:
    pickle.dump(new_d, f)
