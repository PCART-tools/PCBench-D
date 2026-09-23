@tensorrt_converter(acc_ops.asin)
def acc_ops_asin(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.ASIN
    return add_unary_layer(network, input_val, operation_type, name)
