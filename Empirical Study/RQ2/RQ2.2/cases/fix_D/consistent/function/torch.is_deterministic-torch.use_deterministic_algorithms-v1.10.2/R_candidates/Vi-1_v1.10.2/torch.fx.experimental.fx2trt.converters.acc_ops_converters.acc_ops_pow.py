@tensorrt_converter(acc_ops.pow)
def acc_ops_pow(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["exponent"], trt.ElementWiseOperation.POW, name
    )
