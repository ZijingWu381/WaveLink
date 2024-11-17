import torch.nn as nn

class LinearModel(nn.Module):
    def __init__(self, input_dim=4, output_dim=2):
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.linear(x)
        
        
class NLinearModel(nn.Module):
    def __init__(self, input_dim=4, output_dim=2):
        super(NLinearModel, self).__init__()
        self.linear1 = nn.Linear(input_dim, output_dim)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(output_dim, output_dim)

    def forward(self, x):
        # return self.relu(self.linear(x))
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

class ConvNetModel(nn.Module):
    def __init__(self, input_dim=4, output_dim=2):
        super(ConvNetModel, self).__init__()
        # Convolutional layers
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=4, kernel_size=2, stride=1)
        self.relu = nn.ReLU()
        # MLP predictor head
        self.fc1 = nn.Linear(4 * (input_dim - 1), 16)
        self.fc2 = nn.Linear(16, output_dim)

    def forward(self, x):
        # Reshape input x from (batch_size, input_dim) to (batch_size, channels=1, input_dim)
        x = x.unsqueeze(1)  # Shape: (batch_size, 1, input_dim)
        x = self.conv1(x)   # Shape: (batch_size, 4, input_dim - kernel_size + 1)
        x = self.relu(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x