@tensorrt_converter(acc_ops.neg)
def acc_ops_neg(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.NEG
    return add_unary_layer(network, input_val, operation_type, name)
