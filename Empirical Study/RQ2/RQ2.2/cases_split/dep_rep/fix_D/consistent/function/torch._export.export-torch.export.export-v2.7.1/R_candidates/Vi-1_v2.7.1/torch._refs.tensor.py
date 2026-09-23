def tensor(data, *, dtype=None, device=None, pin_memory=False, requires_grad=False):
    # TODO (or not): support names kwarg
    if isinstance(data, torch.Tensor):
        warnings.warn(
            "To copy construct from a tensor, it is recommended to use sourceTensor.detach().clone() "
            "or sourceTensor.detach().clone().requires_grad_(True), rather than torch.tensor(sourceTensor)",
            UserWarning,
            stacklevel=2,
        )
    type_inference = dtype is None
    new_tensor = _internal_new_from_data(
        # device="cpu" because that's what you get with torch.tensor(2) no
        # device by default
        {"device": "cpu"},  # TODO: use torch.get_default_tensor_type
        dtype if dtype is not None else torch.get_default_dtype(),
        device,
        data,
        copy_variables=True,
        copy_numpy=True,
        type_inference=type_inference,
        pin_memory=pin_memory,
    )
    new_tensor.detach_()
    if requires_grad:
        new_tensor.requires_grad_(requires_grad)
    return new_tensor
