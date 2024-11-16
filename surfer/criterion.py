import torch
import torch.nn as nn

def nt_xent_loss(z_i, z_j, temperature=0.5):
    """
    Computes the NT-Xent loss between two sets of embeddings.
    """
    batch_size = z_i.size(0)
    device = z_i.device

    # Normalize embeddings
    z_i = nn.functional.normalize(z_i, dim=1)
    z_j = nn.functional.normalize(z_j, dim=1)

    # Concatenate embeddings
    z = torch.cat([z_i, z_j], dim=0)  # Shape: [2*batch_size, embedding_dim]

    # Compute similarity matrix
    sim_matrix = torch.mm(z, z.T)  # Shape: [2*batch_size, 2*batch_size]
    sim_matrix = sim_matrix / temperature

    # Remove self-similarity scores from the diagonal
    mask = torch.eye(2 * batch_size, dtype=torch.bool).to(device)
    sim_matrix = sim_matrix.masked_fill(mask, -float('inf'))

    # Create labels: positive pairs are diagonal offset by batch_size
    labels = torch.arange(batch_size).to(device)
    labels = torch.cat([labels + batch_size, labels], dim=0)

    # Compute loss
    loss_fn = nn.CrossEntropyLoss()
    loss = loss_fn(sim_matrix, labels)
    return loss