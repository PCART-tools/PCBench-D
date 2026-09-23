@tensorrt_converter(acc_ops.tan)
def acc_ops_tan(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.TAN
    return add_unary_layer(network, input_val, operation_type, name)
