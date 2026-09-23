@tensorrt_converter(acc_ops.maximum)
def acc_ops_maximum(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.MAX, name
    )
