@tensorrt_converter(acc_ops.sinh)
def acc_ops_sinh(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.SINH
    return add_unary_layer(network, input_val, operation_type, name)
