@tensorrt_converter(acc_ops.mul)
def acc_ops_mul(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.PROD, name
    )
