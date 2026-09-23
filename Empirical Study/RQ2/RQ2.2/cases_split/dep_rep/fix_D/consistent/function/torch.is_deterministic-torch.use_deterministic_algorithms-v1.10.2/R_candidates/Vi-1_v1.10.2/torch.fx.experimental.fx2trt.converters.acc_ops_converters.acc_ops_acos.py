@tensorrt_converter(acc_ops.acos)
def acc_ops_acos(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.ACOS
    return add_unary_layer(network, input_val, operation_type, name)
