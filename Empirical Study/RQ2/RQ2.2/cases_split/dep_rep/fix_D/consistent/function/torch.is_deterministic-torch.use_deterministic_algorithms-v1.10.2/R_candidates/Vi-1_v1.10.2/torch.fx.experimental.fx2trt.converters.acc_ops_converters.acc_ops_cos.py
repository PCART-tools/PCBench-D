@tensorrt_converter(acc_ops.cos)
def acc_ops_cos(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.COS
    return add_unary_layer(network, input_val, operation_type, name)
