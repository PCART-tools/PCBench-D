@tensorrt_converter(acc_ops.ceil)
def acc_ops_ceil(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.CEIL
    return add_unary_layer(network, input_val, operation_type, name)
