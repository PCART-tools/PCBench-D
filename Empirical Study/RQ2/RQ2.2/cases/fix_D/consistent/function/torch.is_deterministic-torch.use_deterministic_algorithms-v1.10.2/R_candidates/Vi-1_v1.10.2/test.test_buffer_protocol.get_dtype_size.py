def get_dtype_size(dtype):
    return int(torch.empty((), dtype=dtype).element_size())
