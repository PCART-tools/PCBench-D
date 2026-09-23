def to_numpy(tensor: Optional[torch.Tensor]):
    """
    Convert a PyTorch Tensor to a Numpy Array.
    """
    if tensor is None:
        return tensor

    if tensor.is_quantized:
        tensor = tensor.dequantize()

    assert isinstance(tensor, torch.Tensor), f"to_numpy can't be called on None or a torch.Tensor, got: {tensor}"

    return tensor.cpu().detach().contiguous().numpy()
