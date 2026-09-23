@tensorrt_converter(acc_ops.abs)
def acc_ops_abs(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.ABS
    return add_unary_layer(network, input_val, operation_type, name)
