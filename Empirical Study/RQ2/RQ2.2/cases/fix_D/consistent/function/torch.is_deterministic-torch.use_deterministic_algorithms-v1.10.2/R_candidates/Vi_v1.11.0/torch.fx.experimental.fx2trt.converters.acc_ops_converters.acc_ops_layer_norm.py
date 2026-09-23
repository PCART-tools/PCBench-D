@tensorrt_converter(acc_ops.layer_norm)
def acc_ops_layer_norm(
    network: TRTNetwork,
    target: Target,
    args: Tuple[Argument, ...],
    kwargs: Dict[str, Argument],
    name: str,
) -> Union[TRTTensor, Sequence[TRTTensor]]:
    input_val = kwargs["input"]

    if not isinstance(input_val, TRTTensor):
        raise RuntimeError(f"LayerNorm received input {input_val} that is not part "
                           "of the TensorRT region!")

    shape = kwargs["weight"].shape  # type: ignore[union-attr]
    broadcasted_shape = (1,) * (len(input_val.shape) - len(shape)) + shape
    gamma = to_numpy(kwargs["weight"].reshape(*shape))  # type: ignore[union-attr]
    beta = to_numpy(kwargs["bias"].reshape(*shape))  # type: ignore[union-attr]
    eps = kwargs["eps"]

    axes = 0
    for d in range(len(shape)):
        axes |= 1 << (len(input_val.shape) - d - 1)

    # E[x]
    mean_expected_layer = network.add_reduce(input_val, trt.ReduceOperation.AVG, axes, keep_dims=True)
    set_layer_name(mean_expected_layer, target, f"{name}_mean_expected")

    # X-E[x]
    sub_trt = add_binary_elementwise_layer(
        network, input_val, mean_expected_layer.get_output(0), trt.ElementWiseOperation.SUB, target, f"{name}_sub"
    )
    # Variance = mean(pow(x_sub_mean,2))
    pow_tensor = network.add_constant(
        (1,) * len(input_val.shape), trt.Weights(np.ascontiguousarray([2.0], dtype=np.float32))
    )
    pow_tensor.name = f"{name}_power"
    pow_var = add_binary_elementwise_layer(
        network, sub_trt, pow_tensor.get_output(0), trt.ElementWiseOperation.POW, target, f"{name}_pow_var"
    )
    mean_trt_layer = network.add_reduce(pow_var, trt.ReduceOperation.AVG, axes, keep_dims=True)
    set_layer_name(mean_trt_layer, target, f"{name}_mean")
    # Variance + eps
    eps_tensor = network.add_constant(
        (1,) * len(input_val.shape), trt.Weights(np.ascontiguousarray([eps], dtype=np.float32))
    )
    eps_tensor.name = f"{name}_eps"
    add_trt = add_binary_elementwise_layer(
        network, mean_trt_layer.get_output(0), eps_tensor.get_output(0), trt.ElementWiseOperation.SUM, target, f"{name}_add"
    )
    # SQRT((Var + eps))
    sqrt_trt = add_unary_layer(network, add_trt, trt.UnaryOperation.SQRT, target, f"{name}_sqrt")
    # (x - E[x]) / sqrt((var + eps))
    div_trt = add_binary_elementwise_layer(network, sub_trt, sqrt_trt, trt.ElementWiseOperation.DIV, target, f"{name}_div_trt")

    assert gamma is not None
    gamma_tensor = network.add_constant(gamma.shape, trt.Weights(np.ascontiguousarray(gamma)))  # type: ignore[attr-defined]
    gamma_tensor.name = f"{name}_gamma"
    assert beta is not None
    beta_tensor = network.add_constant(gamma.shape, trt.Weights(np.ascontiguousarray(beta)))  # type: ignore[attr-defined]
    beta_tensor.name = f"{name}_beta"
    # y * gamma + beta
    scale_layer = add_binary_elementwise_layer(
        network, div_trt, gamma_tensor.get_output(0), trt.ElementWiseOperation.PROD, target, f"{name}_scale"
    )
    return add_binary_elementwise_layer(
        network, scale_layer, beta_tensor.get_output(0), trt.ElementWiseOperation.SUM, target, name
    )
