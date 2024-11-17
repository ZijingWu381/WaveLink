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

def np_standardize(X, axis=0):
    return (X - np.mean(X, axis)) / np.std(X, axis)


from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-P', '--pretrained', action='store_true',
                    help="use pretrained model weights")
parser.add_argument('-D', '--data', type=str, nargs='+', help='processed data file name(s)')
# parser.add_argument('-BE', '--beta', type=float, default=1.0, help="beta value for KL loss scaling like in beta-VAE")
# parser.add_argument('-CE', '--ckpt_epochs', type=int, default=0, help="number of epochs trained before resuming training")
# parser.add_argument('-CS', '--category_scales', type=float, nargs='+', help="scaling factor for each category for igr models")
# parser.add_argument('-E', '--epochs', type=int, default=300,
#                     help="number of epochs to train")

args = parser.parse_args()

sys.path.append('../')

np.random.seed(42)
torch.manual_seed(42)

# save paths
current_file_directory = os.path.dirname(os.path.abspath(__file__))
model_save_path = os.path.join(current_file_directory, 'model_ckpts/')
data_paths = [os.path.join(current_file_directory, '../data/processed', d) for d in args.data]

# Hyperparameter: number of components
columns_to_read = [2, 3, 4, 5, 6, 7, 8, 9]  # Example column indices you want to read

# Load the data from the CSV file into a numpy ndarray,
X = []
for path in data_paths:
    X.append(
        np.loadtxt(
            path,
            delimiter=',',
            usecols=columns_to_read
        )
    )
X = np.concatenate(X) 
print('Data shape after removing first row and selecting columns:', X.shape)

# Standardization of data
X = np_standardize(X)

n_samples = len(X)
n_channels = X.shape[1]
t = np.arange(len(X))

# Split the data into training and validation sets (80% train, 20% validation)
X_train, X_val = train_test_split(X, test_size=0.2, random_state=42)


# Hyperparameters
batch_size = 32
epochs = 200
learning_rate = 0.01
temperature = 0.1

# Create Dataset and DataLoader for training and validation
train_dataset = NeuralEEGDataset(X_train)
val_dataset = NeuralEEGDataset(X_val)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# Model training
model = ConvNetModel(input_dim=8)

if not args.pretrained:
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

# Load trained model
checkpoint = torch.load(os.path.join(model_save_path, 'best_model.pth'), weights_only=False)  # Adjust the path if needed
model.load_state_dict(checkpoint)
model.eval()


# #################################
# # Visualization Code
# #################################
visual_length = 1000
# Get embeddings for all data points
with torch.no_grad():
    X_tensor = torch.from_numpy(X).float()[:visual_length]
    embeddings = model(X_tensor)
    # embeddings = nn.functional.normalize(embeddings, dim=1).numpy()
    X_normalized = nn.functional.normalize(X_tensor, dim=1).numpy()

# Plot first two channels of data
plt.figure(figsize=(8, 6))
plt.scatter(X_tensor[:, 0], X_tensor[:, 1], c=t[:visual_length], cmap='viridis')
plt.colorbar(label='Time')
plt.xlabel('Channel 1')
plt.ylabel('Channel 2')
plt.title('First two channels data')
plt.show()

# Plot first two channels of data normalized
plt.figure(figsize=(8, 6))
plt.scatter(X_normalized[:, 0], X_normalized[:, 1], c=t[:visual_length], cmap='viridis')
plt.colorbar(label='Time')
plt.xlabel('Channel 1')
plt.ylabel('Channel 2')
plt.title('First two channels data - Normalized')
plt.show()


# Plot last two channels of data
plt.figure(figsize=(8, 6))
plt.scatter(X_tensor[:, 2], X_tensor[:, 3], c=t[:visual_length], cmap='viridis')
plt.colorbar(label='Time')
plt.xlabel('Channel 3')
plt.ylabel('Channel 4')
plt.title('Second two channels data')
plt.show()

from sklearn.decomposition import PCA  # Make sure to import PCA

# Perform PCA on the normalized data
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_normalized)

# Plot the first two principal components
plt.figure(figsize=(8, 6))
plt.scatter(
    principal_components[:, 0],
    principal_components[:, 1],
    c=t[:visual_length],
    cmap='viridis'
)
plt.colorbar(label='Time')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('First Two Principal Components of Data')
plt.show()


# Plot the embeddings
plt.figure(figsize=(8, 6))
plt.scatter(embeddings[:, 0], embeddings[:, 1], c=t[:visual_length], cmap='viridis')
plt.colorbar(label='Time')
plt.xlabel('Embedding Dimension 1')
plt.ylabel('Embedding Dimension 2')
plt.title('Learned 2D Representations')
plt.show()

