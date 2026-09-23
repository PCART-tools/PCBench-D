def filter_requires_grad(tensors):
    return [t for t in tensors if t.requires_grad]
