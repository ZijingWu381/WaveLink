import numpy as np

def np_standardize(X, axis=0):
    return (X - np.mean(X, axis)) / np.std(X, axis)
