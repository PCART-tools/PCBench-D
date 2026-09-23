@tensorrt_converter(acc_ops.floor)
def acc_ops_floor(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.FLOOR
    return add_unary_layer(network, input_val, operation_type, name)
