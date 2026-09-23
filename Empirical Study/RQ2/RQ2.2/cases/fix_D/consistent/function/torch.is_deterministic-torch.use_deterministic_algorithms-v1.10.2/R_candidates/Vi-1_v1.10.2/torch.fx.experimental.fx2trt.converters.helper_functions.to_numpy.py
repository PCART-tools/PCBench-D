def to_numpy(tensor: torch.Tensor):
    """
    Convert a PyTorch Tensor to a Numpy Array.
    """
    if tensor is None:
        return tensor

    if tensor.is_quantized:
        tensor = tensor.dequantize()

    return tensor.cpu().detach().contiguous().numpy()
