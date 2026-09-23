def to_numpy(tensor: Optional[torch.Tensor]) -> Optional[np.ndarray]:
    """
    Convert a PyTorch Tensor to a Numpy Array. If the tensor is
    quantized it will be dequantized first.

    Args:
        tensor (Optional[torch.Tensor]): A PyTorch tensor or None.

    Returns:
        A Numpy array.
    """

    if tensor is None:
        return tensor

    assert isinstance(tensor, torch.Tensor), f"to_numpy can only be called on None or a torch.Tensor, got: {tensor}"
    if tensor.is_quantized:
        tensor = tensor.dequantize()

    return tensor.cpu().detach().contiguous().numpy()
