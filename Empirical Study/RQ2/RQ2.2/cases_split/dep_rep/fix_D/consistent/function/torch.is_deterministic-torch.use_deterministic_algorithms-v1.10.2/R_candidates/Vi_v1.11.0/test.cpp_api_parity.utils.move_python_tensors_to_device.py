def move_python_tensors_to_device(python_tensors, device):
    return [tensor.to(device) for tensor in python_tensors]
