@tensorrt_converter(acc_ops.matmul)
def acc_ops_matmul(network, target, args, kwargs, name):
    input_val = get_trt_tensor(network, kwargs["input"], f"{name}_input")
    other_val = get_trt_tensor(network, kwargs["other"], f"{name}_other")

    for i in [input_val, other_val]:
        if not isinstance(i, trt.tensorrt.ITensor):
            raise RuntimeError(
                f"matmul received input {i} that is not part " "of the TensorRT region!"
            )

    return add_matrix_multiply_layer(network, input_val, other_val, name)
