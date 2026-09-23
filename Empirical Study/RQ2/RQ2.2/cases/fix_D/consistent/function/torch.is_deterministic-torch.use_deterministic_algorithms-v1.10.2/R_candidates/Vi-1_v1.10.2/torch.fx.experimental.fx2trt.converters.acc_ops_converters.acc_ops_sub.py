@tensorrt_converter(acc_ops.sub)
def acc_ops_sub(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.SUB, name
    )
