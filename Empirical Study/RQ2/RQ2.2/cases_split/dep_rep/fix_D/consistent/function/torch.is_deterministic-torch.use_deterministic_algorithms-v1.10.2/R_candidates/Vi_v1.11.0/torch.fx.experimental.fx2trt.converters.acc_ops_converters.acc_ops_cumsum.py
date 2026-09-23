@tensorrt_converter(acc_ops.cumsum, no_implicit_batch_dim=True)
def acc_ops_cumsum(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]
    dim = cast(int, kwargs["dim"])
    input_shape = input_val.shape  # type: ignore[union-attr]
    input_dim_size = len(input_val.shape)  # type: ignore[union-attr]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"cumsum received input {input_val} that is not part "
                           "of the TensorRT region!")
    if network.has_implicit_batch_dimension:
        raise RuntimeError(
            "cumsum converter currently doesn't support implicit batch dimension"
        )
    dim = get_positive_dim(dim, input_dim_size)
    loop = network.add_loop()
    trip_limit = None
    if (input_shape[dim] > 0):
        axis = torch.tensor(input_shape[dim], dtype=torch.int32)
        trip_limit_layer = network.add_constant(axis.shape, to_numpy(axis))
    else:
        input_shape = network.add_shape(input_val).get_output(0)
        dim_value = torch.tensor(dim, dtype=torch.int32)
        axis = network.add_constant(dim_value.shape, to_numpy(dim_value)).get_output(0)
        trip_limit_layer = network.add_gather(input_shape, axis, 0)
    set_layer_name(trip_limit_layer, target, f"{name}_trip_limit")
    trip_limit = trip_limit_layer.get_output(0)

    loop.add_trip_limit(trip_limit, trt.TripLimit(0))
    iterator = loop.add_iterator(input_val, dim, False)
    data = iterator.get_output(0)
    new_dims = tuple(data.shape)
    zero_tensor = torch.zeros(new_dims, dtype=torch.float32)
    zero_tensor = network.add_constant(zero_tensor.shape, to_numpy(zero_tensor)).get_output(0)

    running_sum = loop.add_recurrence(zero_tensor)
    set_layer_name(running_sum, target, f"{name}_running_sum_1")
    running_sum_tensor = running_sum.get_output(0)

    current_sum = add_binary_elementwise_layer(
        network, data, running_sum_tensor, trt.ElementWiseOperation.SUM, target, f"{name}_sum_1"
    )
    running_sum.set_input(1, current_sum)

    running_sum = loop.add_recurrence(zero_tensor)
    set_layer_name(running_sum, target, f"{name}_running_sum_2")
    running_sum_tensor = running_sum.get_output(0)

    current_sum = add_binary_elementwise_layer(
        network, data, running_sum_tensor, trt.ElementWiseOperation.SUM, target, f"{name}_sum_2"
    )
    running_sum.set_input(1, current_sum)

    loop_output = loop.add_loop_output(current_sum, trt.LoopOutput.CONCATENATE, dim)
    set_layer_name(loop_output, target, f"{name}_loop_output")
    loop_output.set_input(1, trip_limit)
    return loop_output.get_output(0)
