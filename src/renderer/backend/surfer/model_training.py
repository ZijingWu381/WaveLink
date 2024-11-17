import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from models import ConvNetModel
from criterion import nt_xent_loss
from dataset import NeuralEEGDataset

import sys
import os

sys.path.append('../')

np.random.seed(42)
torch.manual_seed(42)

# save paths
model_save_path = 'model_ckpts/'
data_path = '../data/'

# Hyperparameter: number of components
columns_to_read = [0, 1, 6, 7]  # Example column indices you want to read

# Load the data from the CSV file into a numpy ndarray,
# skipping the first row and using specified columns
X_all = np.loadtxt(
    os.path.join(data_path, 'preprocessed_eeg_data.csv'),
    delimiter=',',
    skiprows=1,
    usecols=columns_to_read
)
print('Data shape after removing first row and selecting columns:', X_all.shape)

X = X_all

n_samples = len(X)
n_channels = X.shape[1]
t = np.arange(len(X))
time_length = 2 # segment the data with the time length we want,
                # in secs

# Split the data into training and validation sets (80% train, 20% validation)
X_train, X_val = train_test_split(X, test_size=0.2, random_state=42)


# Hyperparameters
batch_size = 32
epochs = 40
learning_rate = 0.01
temperature = 0.5

# Create Dataset and DataLoader for training and validation
train_dataset = NeuralEEGDataset(X_train)
val_dataset = NeuralEEGDataset(X_val)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


# Initialize model, optimizer
model = ConvNetModel()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


# Initialize variables for tracking best validation loss
best_val_loss = float('inf')

for epoch in range(epochs):
    model.train()  # Set model to training mode
    total_loss = 0
    for x_i, x_j in train_dataloader:
        # Forward pass through the model
        z_i = model(x_i)
        z_j = model(x_j)

        # Compute loss
        loss = nt_xent_loss(z_i, z_j, temperature)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_dataloader)
    print(f"Epoch [{epoch+1}/{epochs}], Training Loss: {avg_loss:.4f}")

    # Evaluate on validation set
    model.eval()  # Set model to evaluation mode
    val_loss = 0
    with torch.no_grad():
        for x_i, x_j in val_dataloader:
            z_i = model(x_i)
            z_j = model(x_j)
            # Compute loss
            loss = nt_xent_loss(z_i, z_j, temperature)
            val_loss += loss.item()
    val_loss /= len(val_dataloader)
    print(f"Validation Loss: {val_loss:.4f}")

    # Check if this is the best validation loss so far
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        # Save the model
        torch.save(model.state_dict(), os.path.join(model_save_path, 'best_model.pth'))
        print("Model saved.")

# #################################
# # Visualization Code
# #################################
# visual_length = 200
# # Get embeddings for all data points
# with torch.no_grad():
#     X_tensor = torch.from_numpy(X).float()[:visual_length]
#     embeddings = model(X_tensor)
#     # embeddings = nn.functional.normalize(embeddings, dim=1).numpy()
#     X_normalized = nn.functional.normalize(X_tensor, dim=1).numpy()

# # Plot first two channels of data
# plt.figure(figsize=(8, 6))
# plt.scatter(X_tensor[:, 0], X_tensor[:, 1], c=t[:visual_length], cmap='viridis')
# plt.colorbar(label='Time')
# plt.xlabel('Channel 1')
# plt.ylabel('Channel 2')
# plt.title('First two channels data')
# plt.show()

# # Plot first two channels of data normalized
# plt.figure(figsize=(8, 6))
# plt.scatter(X_normalized[:, 0], X_normalized[:, 1], c=t[:visual_length], cmap='viridis')
# plt.colorbar(label='Time')
# plt.xlabel('Channel 1')
# plt.ylabel('Channel 2')
# plt.title('First two channels data - Normalized')
# plt.show()

# from sklearn.decomposition import PCA  # Make sure to import PCA

# # Perform PCA on the normalized data
# pca = PCA(n_components=2)
# principal_components = pca.fit_transform(X_normalized)

# # Plot the first two principal components
# plt.figure(figsize=(8, 6))
# plt.scatter(
#     principal_components[:, 0],
#     principal_components[:, 1],
#     c=t[:200],
#     cmap='viridis'
# )
# plt.colorbar(label='Time')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.title('First Two Principal Components of Data')
# plt.show()


# # Plot the embeddings
# plt.figure(figsize=(8, 6))
# plt.scatter(embeddings[:, 0], embeddings[:, 1], c=t[:visual_length], cmap='viridis')
# plt.colorbar(label='Time')
# plt.xlabel('Embedding Dimension 1')
# plt.ylabel('Embedding Dimension 2')
# plt.title('Learned 2D Representations')
# plt.show()

