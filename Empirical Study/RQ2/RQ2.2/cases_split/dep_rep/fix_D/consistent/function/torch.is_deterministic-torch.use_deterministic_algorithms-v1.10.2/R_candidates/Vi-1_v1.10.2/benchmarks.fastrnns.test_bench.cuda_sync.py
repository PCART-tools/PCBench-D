def cuda_sync(func, *args, **kwargs):
    out = func(*args, **kwargs)
    torch.cuda.synchronize()
    return out
