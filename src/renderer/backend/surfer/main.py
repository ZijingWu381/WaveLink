"""
This is the main running script. It applies the trained self-supervised 
contrastive learning model to perform feature extraction on the 
data time series pair. Then it applies CCA to compute the correlation
as the similarity measurement.

"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA

import torch
import torch.nn as nn

from models import ConvNetModel

import sys
import os


sys.path.append('../')

def main():
    np.random.seed(42)
    torch.manual_seed(42)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, 'tempdata')

    # save paths
    model_save_path = os.path.join(current_dir, 'model_ckpts')

    # Hyperparameter: number of components
    n_components = 2  # Change this value as needed
    sample_rate = 50 


    ################
    # Data Loading #
    ################
    columns_to_read = [0, 1, 6, 7]  # Example column indices you want to read

    # Load the data from the CSV file into a numpy ndarray,
    # skipping the first row and using specified columns
    X_all = np.loadtxt(
        os.path.join(data_path, 'data_output_1.csv'),
        delimiter=',',
        skiprows=1,
        usecols=columns_to_read
    )

    Y_all = np.loadtxt(
        os.path.join(data_path, 'data_output_2.csv'),
        delimiter=',',
        skiprows=1,
        usecols=columns_to_read
    )

    print('Data shape after removing first row and selecting columns:', X_all.shape)

    # # make the Y data out of X by shift by 0.5 seconds
    # # TODO create loading for the separate data Y_all
    # Y_all = np.concatenate([X_all[25:, :], X_all[:25, :]])


    ######################
    # Feature Extraction #
    ######################
    X = torch.from_numpy(X_all).float()
    Y = torch.from_numpy(Y_all).float()


    n_samples = len(X)
    n_channels = X.shape[1]
    t = np.arange(len(X))

    # Initialize model, optimizer
    model = ConvNetModel()
    checkpoint = torch.load(os.path.join(model_save_path, 'best_model.pth'), weights_only=False)  # Adjust the path if needed
    model.load_state_dict(checkpoint)
    model.eval()

    X_feats = model(X)
    Y_feats = model(Y)

    ########################
    # Correlation Analysis #
    ########################
    X_feats = X_feats.detach().numpy()
    Y_feats = Y_feats.detach().numpy()

    # store the correlations overtime
    t = np.arange(len(X_feats))

    # Initialize and fit the CCA model
    cca = CCA(n_components=n_components)
    cca.fit(X_feats, Y_feats)
    X_c, Y_c = cca.transform(X_feats, Y_feats)

    # Calculate the canonical correlation coefficients
    canonical_corrs = [np.corrcoef(X_c[:, i], Y_c[:, i])[0, 1] for i in range(n_components)]
    print(canonical_corrs)
    return canonical_corrs[0]

    # # Plot the original X and Y data
    # fig, axs = plt.subplots(n_channels, 2, figsize=(12, 8))

    # for i in range(n_channels):
    #     axs[i, 0].plot(t, X[:, i])
    #     axs[i, 0].set_title(f'X Channel {i+1}')
    #     axs[i, 0].set_xlabel('Time')
    #     axs[i, 0].set_ylabel('Amplitude')

    #     axs[i, 1].plot(t, Y[:, i], color='orange')
    #     axs[i, 1].set_title(f'Y Channel {i+1}')
    #     axs[i, 1].set_xlabel('Time')
    #     axs[i, 1].set_ylabel('Amplitude')

    # plt.tight_layout()
    # plt.show()

    # # Plot the transformed canonical components over time
    # fig, axs = plt.subplots(n_components, 1, figsize=(12, 4 * n_components))

    # for i in range(n_components):
    #     axs[i].plot(t, X_c[:, i], label=f'Transformed X Component {i+1}')
    #     axs[i].plot(t, Y_c[:, i], label=f'Transformed Y Component {i+1}')
    #     axs[i].set_xlabel('Time')
    #     axs[i].set_ylabel('Canonical Component Value')
    #     axs[i].set_title(f'Canonical Components {i+1} over Time')
    #     axs[i].legend()

    # plt.tight_layout()
    # plt.show()


