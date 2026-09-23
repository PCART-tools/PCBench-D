@tensorrt_converter(acc_ops.cosh)
def acc_ops_cosh(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.COSH
    return add_unary_layer(network, input_val, operation_type, name)
