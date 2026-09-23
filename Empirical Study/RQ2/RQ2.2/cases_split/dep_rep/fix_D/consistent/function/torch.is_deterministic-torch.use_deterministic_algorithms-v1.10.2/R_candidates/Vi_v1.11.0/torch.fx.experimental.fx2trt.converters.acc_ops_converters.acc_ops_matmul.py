@tensorrt_converter(acc_ops.matmul)
def acc_ops_matmul(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = get_trt_tensor(network, kwargs["input"], f"{name}_input")
    other_val = get_trt_tensor(network, kwargs["other"], f"{name}_other")

    for i in [input_val, other_val]:
        if not isinstance(i, TRTTensor):
            raise RuntimeError(
                f"matmul received input {i} that is not part of the TensorRT region!"
            )

    input_matrix_op = other_matrix_op = trt.MatrixOperation.NONE
    preset_diff = 0

    if len(input_val.shape) == 1:
        preset_diff -= 1
        input_matrix_op = trt.MatrixOperation.VECTOR

    if len(other_val.shape) == 1:
        preset_diff += 1
        other_matrix_op = trt.MatrixOperation.VECTOR

    input_val, other_val = broadcast(network, input_val, other_val, f"{name}_input", f"{name}_other", preset_diff)
    layer = network.add_matrix_multiply(input_val, input_matrix_op, other_val, other_matrix_op)
    set_layer_name(layer, target, name)
    return layer.get_output(0)
