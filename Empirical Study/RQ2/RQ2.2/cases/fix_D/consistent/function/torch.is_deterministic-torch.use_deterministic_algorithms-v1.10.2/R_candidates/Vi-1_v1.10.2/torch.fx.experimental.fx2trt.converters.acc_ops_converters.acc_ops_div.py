@tensorrt_converter(acc_ops.div)
def acc_ops_div(network, target, args, kwargs, name):
    return add_binary_elementwise_layer(
        network, kwargs["input"], kwargs["other"], trt.ElementWiseOperation.DIV, name
    )
