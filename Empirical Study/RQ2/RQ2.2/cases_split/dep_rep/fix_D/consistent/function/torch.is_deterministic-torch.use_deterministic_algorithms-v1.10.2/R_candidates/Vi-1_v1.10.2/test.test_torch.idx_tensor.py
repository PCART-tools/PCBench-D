def idx_tensor(size, max_val):
    return torch.LongTensor(*size).random_(0, max_val - 1)
