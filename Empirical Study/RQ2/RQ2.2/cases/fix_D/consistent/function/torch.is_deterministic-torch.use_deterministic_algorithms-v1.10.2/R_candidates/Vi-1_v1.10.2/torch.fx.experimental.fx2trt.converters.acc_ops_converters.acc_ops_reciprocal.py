@tensorrt_converter(acc_ops.reciprocal)
def acc_ops_reciprocal(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.RECIP
    return add_unary_layer(network, input_val, operation_type, name)
