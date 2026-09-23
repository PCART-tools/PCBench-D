def set_python_tensors_requires_grad(python_tensors):
    return [tensor.requires_grad_(True) if tensor.dtype != torch.long else tensor for tensor in python_tensors]
