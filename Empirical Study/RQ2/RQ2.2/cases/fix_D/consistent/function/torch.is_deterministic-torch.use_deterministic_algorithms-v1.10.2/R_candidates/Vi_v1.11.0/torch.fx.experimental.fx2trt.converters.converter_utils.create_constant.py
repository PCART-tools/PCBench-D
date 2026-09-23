def create_constant(
    network: TRTNetwork,
    value: Union[int, float, torch.Tensor],
    name: str,
    dtype: Optional[torch.dtype],
) -> TRTTensor:
    """
    Add a TensorRT constant layer whose value is `value` to `network`.

    Args:
        network (TRTNetwork): A TensorRT network to which we want to add
            a constant layer.
        value (Union[int, float, torch.Tensor]): A literal value or a PyTorch tensor
            that will be used as value of the added TensorRT Constant layer.
        name (str): Name of the added TensorRT Constant layer.
        dtype (Optional[torch.dtype]): If a dtype is given, we will convert the type
            of the given `value` to this dtype.

    Returns:
        A TensorRT ITensor that represents the given value.
    """
    if isinstance(value, int):
        value = torch.IntTensor([value])

    if isinstance(value, float):
        value = torch.Tensor([value])

    if dtype:
        value = value.to(dtype)

    constant = network.add_constant(value.shape, to_numpy(value))
    constant.name = name
    return constant.get_output(0)
