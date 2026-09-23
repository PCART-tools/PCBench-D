def save(tensors, *args, **kwargs):
    torch.save(to_cpu(tensors), *args, **kwargs)
