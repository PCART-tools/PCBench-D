@tensorrt_converter(acc_ops.getitem)
def acc_ops_getitem(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    slices = kwargs["idx"]

    if not isinstance(input_val, TRTTensor):
        return operator.getitem(input_val, slices)  # type: ignore[arg-type]

    assert not has_dynamic_shape(
        input_val.shape
    ), "Currently we don't support slicing tensor if it has dynamic shape."

    def num_slice_types(slices):
        """
        Gather the number of slice in getitem slices.
        """
        num_slice = 0
        for s in slices:
            if isinstance(s, slice) or isinstance(s, int):
                num_slice += 1
        return num_slice

    def slice_to_trt_params(py_slice, dim_size):
        """
        Convert python slice to TensorRT slice layer parameters.
        """
        start = get_positive_dim(py_slice.start, dim_size) if py_slice.start else 0
        stride = py_slice.step if py_slice.step else 1
        stop = get_positive_dim(py_slice.stop, dim_size) if py_slice.stop else dim_size
        size = math.ceil((stop - start) * 1.0 / stride)
        return start, size, stride

    if not isinstance(slices, tuple) and not isinstance(slices, list):
        slices = (slices,)

    if network.has_implicit_batch_dimension:
        # Raise an error if it's trying to subscript batch dimension unless it's
        # slice(None, None, None).
        batch_subscript = slices[0]
        if batch_subscript not in [slice(None, None, None), slice(0, None, None)]:
            raise RuntimeError(
                f"{name}: Can't subscript batch dimension when it's implicit. Got {slices}"
            )

        # Remove batch_dim subscript
        slices = slices[1:]

    # Replace ellipsis with expanded slices.
    # Compute the number of dim ellipsis represent.
    num_ellipsis = len(input_val.shape) - num_slice_types(slices)
    new_slices = []
    for s in slices:
        if s == Ellipsis:
            while num_ellipsis > 0:
                new_slices.append(slice(None, None, None))
                num_ellipsis -= 1
        else:
            new_slices.append(s)
    slices = new_slices

    # Build trt slice layer params
    start = []
    size = []
    stride = []

    i = 0
    for s in slices:
        if s is None:
            continue

        if isinstance(s, slice):
            params = slice_to_trt_params(s, input_val.shape[i])
            start.append(params[0])
            size.append(params[1])
            stride.append(params[2])
        else:
            start.append(get_positive_dim(s, input_val.shape[i]))
            size.append(1)
            stride.append(1)
        i += 1

    while i < len(input_val.shape):
        start.append(0)
        size.append(input_val.shape[i])
        stride.append(1)
        i += 1

    layer = network.add_slice(
        input=input_val,
        start=start,
        shape=size,
        stride=stride,
    )
    set_layer_name(layer, target, name)

    # Add shuffle layer to insert dimensions for 'None' and remove dimensions for 'int'.
    if any(not isinstance(s, slice) for s in slices):
        slice_out = layer.get_output(0)
        layer = network.add_shuffle(slice_out)
        set_layer_name(layer, target, f"{name}_shuffle")
        final_shape = []
        original_idx = 0
        for s in slices:
            # If it's a slice, keep the dim.
            if isinstance(s, slice):
                final_shape.append(slice_out.shape[original_idx])
                original_idx += 1
            # If it's None, extend the dim.
            elif s is None:
                final_shape.append(1)
            # If it's a int, remove the dim.
            else:
                original_idx += 1
        layer.reshape_dims = tuple(final_shape) + tuple(slice_out.shape)[original_idx:]

    return layer.get_output(0)
