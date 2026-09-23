@tensorrt_converter(acc_ops.sqrt)
def acc_ops_sqrt(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.SQRT
    return add_unary_layer(network, input_val, operation_type, name)
