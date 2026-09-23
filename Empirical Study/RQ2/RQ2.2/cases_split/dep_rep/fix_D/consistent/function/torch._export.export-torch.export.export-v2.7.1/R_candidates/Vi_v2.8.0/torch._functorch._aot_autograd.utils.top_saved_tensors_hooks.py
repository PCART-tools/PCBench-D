def top_saved_tensors_hooks():
    return torch._C._autograd._top_saved_tensors_default_hooks(True)
