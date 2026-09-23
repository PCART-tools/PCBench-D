@tensorrt_converter(acc_ops.minimum)
def acc_ops_minimum(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.MIN, name
    )
