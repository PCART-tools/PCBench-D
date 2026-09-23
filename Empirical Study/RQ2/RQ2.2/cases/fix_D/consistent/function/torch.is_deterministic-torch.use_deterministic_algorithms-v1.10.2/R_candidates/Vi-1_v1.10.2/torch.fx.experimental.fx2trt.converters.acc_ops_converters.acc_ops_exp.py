@tensorrt_converter(acc_ops.exp)
def acc_ops_exp(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.EXP
    return add_unary_layer(network, input_val, operation_type, name)
