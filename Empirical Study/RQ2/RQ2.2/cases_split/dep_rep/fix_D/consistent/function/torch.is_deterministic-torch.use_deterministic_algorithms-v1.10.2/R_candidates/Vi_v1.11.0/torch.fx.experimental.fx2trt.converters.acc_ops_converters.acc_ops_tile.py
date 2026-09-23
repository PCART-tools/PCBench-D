@tensorrt_converter(acc_ops.tile)
def acc_ops_tile(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"tile received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    dims = tuple(cast(Sequence[int], kwargs["dims"]))
    n_input_dims = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)

    if len(dims) > n_input_dims:
        assert not network.has_implicit_batch_dimension
        layer = network.add_shuffle(input_val)
        layer.name = f"{name}_reshape"
        num_preceding_ones = len(dims) - n_input_dims

        if len(get_dynamic_dims(input_val.shape)) > 1:
            input_shape_layer = network.add_shape(input_val)
            input_shape_layer.name = f"{name}_input_shape"
            preceding_ones = network.add_constant(
                (num_preceding_ones,), np.ascontiguousarray([1] * num_preceding_ones, np.int32)
            ).get_output(0)
            reshape_layer = network.add_concatenation([preceding_ones, input_shape_layer.get_output(0)])
            reshape_layer.axis = 0
            reshape_layer.name = f"{name}_reshape_dims"
            layer.set_input(1, reshape_layer.get_output(0))
        else:
            layer.reshape_dims = (1,) * (len(dims) - n_input_dims) + tuple(input_val.shape)
        input_val = layer.get_output(0)
    else:
        dims = (1,) * (n_input_dims - len(dims)) + dims

    if network.has_implicit_batch_dimension:
        assert dims[0] == 1, "Can't tile the batch dim when it's implicit."
        dims = dims[1:]

    starts = [0] * len(dims)
    shapes = [i * j for i, j in zip(input_val.shape, dims)]  # type: ignore[union-attr]
    # If there's dynmaic dim then there would be negative dims in shapes which is not allowed.
    # Here we build a dummy shapes array.
    if has_dynamic_shape(input_val.shape):  # type: ignore[union-attr]
        shapes = [1] * len(dims)
    strides = [1] * len(dims)
    layer = network.add_slice(input_val, starts, shapes, strides)
    layer.mode = trt.SliceMode.WRAP
    set_layer_name(layer, target, name)

    if has_dynamic_shape(input_val.shape):  # type: ignore[union-attr]
        starts_tensor = network.add_constant(
            (len(dims),), np.ascontiguousarray([0] * len(dims), np.int32)
        ).get_output(0)
        dims_tensor = network.add_constant(
            (len(dims),), np.ascontiguousarray(dims, np.int32)
        ).get_output(0)
        input_shape_layer = network.add_shape(input_val)
        input_shape_layer.name = f"{name}_slice_input_shape"
        slice_shapes_tensor = add_binary_elementwise_layer(
            network,
            input_shape_layer.get_output(0),
            dims_tensor,
            trt.ElementWiseOperation.PROD,
            target,
            f"{name}_slice_shapes",
        )
        layer.set_input(1, starts_tensor)
        layer.set_input(2, slice_shapes_tensor)

    return layer.get_output(0)
