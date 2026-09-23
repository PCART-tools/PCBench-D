@tensorrt_converter(acc_ops.log)
def acc_ops_log(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.UnaryOperation.LOG
    return add_unary_layer(network, input_val, operation_type, name)
