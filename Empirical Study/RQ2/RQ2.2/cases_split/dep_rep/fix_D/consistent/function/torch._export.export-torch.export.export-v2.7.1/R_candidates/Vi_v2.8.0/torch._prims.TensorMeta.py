def TensorMeta(
    tensorlike: Optional[Union[NumberType, torch.Tensor]] = None,
    *,
    shape: Optional[ShapeType] = None,
    strides: Optional[StrideType] = None,
    dtype: Optional[torch.dtype] = None,
    device: Optional[Union[torch.device, str]] = None,
):
    if isinstance(tensorlike, Number):
        assert not shape and (shape is None or isinstance(shape, Sequence))
        assert not strides and (strides is None or isinstance(strides, Sequence))
        inferred_shape: tuple[int, ...] = ()
        inferred_strides: tuple[int, ...] = ()
        inferred_dtype = type_to_dtype(type(tensorlike))
        inferred_device = torch.device("cpu")
        # TODO: This looks wrong, a number that is wrapped into a tensor
        # needs to behave differently than a scalar tensor for type
        # promotion purposes
    elif tensorlike is not None:
        assert isinstance(tensorlike, torch.Tensor)
        inferred_shape = tuple(tensorlike.shape)
        inferred_strides = tuple(tensorlike.stride())
        inferred_dtype = tensorlike.dtype
        inferred_device = tensorlike.device
    else:
        # If no tensorlike "example" is given then all metadata
        # must be provided explicitly
        assert shape is not None
        assert strides is not None
        assert dtype is not None
        assert device is not None

    shape = inferred_shape if shape is None else tuple(shape)  # type: ignore[possibly-undefined]
    strides = inferred_strides if strides is None else tuple(strides)  # type: ignore[possibly-undefined]
    dtype = inferred_dtype if dtype is None else dtype  # type: ignore[possibly-undefined]
    device = inferred_device if device is None else device  # type: ignore[possibly-undefined]

    if isinstance(device, str):
        device = torch.device(device)

    return torch.empty_strided(shape, strides, dtype=dtype, device=device)
