@tensorrt_converter(acc_ops.reshape)
def acc_ops_reshape(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(
            f"Reshape received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    shape = TensorMetadata(*kwargs["acc_out_ty"]).shape  # type: ignore[misc]
    if network.has_implicit_batch_dimension:
        shape = shape[1:]

    layer = network.add_shuffle(input_val)

    if all(isinstance(s, int) for s in shape):
        layer.reshape_dims = tuple(shape)
    else:
        # Convert all the dimensions to trt Tensors.
        trt_shape = []

        for i, s in enumerate(shape):
            if isinstance(s, TRTTensor):
                if len(s.shape) == 0:
                    s = prepend_ones(network, s, f"{name}_{i}", 1)
                trt_shape.append(s)
            else:
                trt_shape.append(
                    get_trt_tensor(network, s, f"{name}_{i}")
                )

        shape_layer = network.add_concatenation(inputs=trt_shape)
        shape_layer.axis = 0
        shape_layer.name = f"{name}_output_shape"
        layer.set_input(1, shape_layer.get_output(0))

    set_layer_name(layer, target, name)
    return layer.get_output(0)
