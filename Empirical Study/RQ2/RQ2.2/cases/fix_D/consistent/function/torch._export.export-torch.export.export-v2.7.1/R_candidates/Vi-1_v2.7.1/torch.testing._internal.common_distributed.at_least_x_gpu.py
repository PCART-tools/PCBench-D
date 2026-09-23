def at_least_x_gpu(x):
    return torch.cuda.is_available() and torch.cuda.device_count() >= x
