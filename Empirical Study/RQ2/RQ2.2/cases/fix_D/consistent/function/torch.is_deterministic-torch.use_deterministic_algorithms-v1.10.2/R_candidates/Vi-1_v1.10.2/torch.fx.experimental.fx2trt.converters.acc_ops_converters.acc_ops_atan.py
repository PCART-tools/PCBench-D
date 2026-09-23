@tensorrt_converter(acc_ops.atan)
def acc_ops_atan(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.ATAN
    return add_unary_layer(network, input_val, operation_type, name)
