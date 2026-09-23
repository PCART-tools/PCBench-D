@tensorrt_converter(acc_ops.add)
def acc_ops_add(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.SUM, name
    )
