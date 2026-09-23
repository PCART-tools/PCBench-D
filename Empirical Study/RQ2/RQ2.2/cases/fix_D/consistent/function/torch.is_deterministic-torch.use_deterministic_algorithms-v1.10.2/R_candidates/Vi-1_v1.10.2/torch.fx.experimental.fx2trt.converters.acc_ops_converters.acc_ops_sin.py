@tensorrt_converter(acc_ops.sin)
def acc_ops_sin(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.SIN
    return add_unary_layer(network, input_val, operation_type, name)
