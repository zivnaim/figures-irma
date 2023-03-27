import os
import pickle

dirs = ["./new_seeds_pep5", "./new_seeds_pep7", "./original_combine"]
names = ["count.pkl", "f1.pkl", "precision.pkl", "recall.pkl", "times.pkl"]

for name in names:
    new_d = {}
    for dir in dirs:
        path = os.path.join(dir, name)
        with open(path, "rb") as f:
            d = pickle.load(f)
            new_d.update(d)
    
    with open(name, "wb") as f:
        pickle.dump(new_d, f)

            