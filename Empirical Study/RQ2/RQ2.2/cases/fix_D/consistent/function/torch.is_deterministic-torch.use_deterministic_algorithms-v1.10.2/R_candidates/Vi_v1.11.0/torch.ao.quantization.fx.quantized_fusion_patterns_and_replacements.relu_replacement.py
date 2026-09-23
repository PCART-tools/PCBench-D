def relu_replacement(x, scale, zero_point):
    x = torch.nn.functional.relu(x)
    return x
