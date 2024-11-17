import random
import torch
from torch.utils.data import Dataset


class NeuralEEGDataset(Dataset):
    def __init__(self, X, noise_level=0.1):
        self.X = X
        self.noise_level = noise_level

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        x = self.X[idx]
        x = torch.from_numpy(x).float()
        # Create two augmented versions of x
        x_i = self.augment(x.clone().detach())
        x_j = self.augment(x.clone().detach())
        return x_i, x_j

    def augment(self, x):
        # Apply a series of random augmentations
        augmentations = [
            self.add_gaussian_noise,
            self.scaling,
            self.time_shifting,
            self.channel_shuffling,
            self.channel_dropping,
        ]

        # Randomly select augmentations to apply
        num_augmentations = random.randint(1, 3)  # Apply 1 to 3 augmentations
        augmentation_functions = random.sample(augmentations, num_augmentations)

        for func in augmentation_functions:
            x = func(x)

        return x

    def add_gaussian_noise(self, x):
        noise = torch.randn_like(x) * self.noise_level
        return x + noise

    def scaling(self, x):
        scaling_factor = random.uniform(0.8, 1.2)  # Scale between 80% and 120%
        return x * scaling_factor

    def time_shifting(self, x):
        shift = random.randint(-2, 2)  # Shift by up to 2 time steps
        x = torch.roll(x, shifts=shift, dims=0)
        return x

    def channel_shuffling(self, x):
        channel_indices = torch.randperm(x.size(0))
        return x[channel_indices]

    def channel_dropping(self, x):
        num_channels = x.size(0)
        num_drop = random.randint(1, num_channels - 1)  # Drop at least one channel
        drop_indices = random.sample(range(num_channels), num_drop)
        x[drop_indices] = 0  # Set dropped channels to zero
        return x