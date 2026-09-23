@tensorrt_converter(acc_ops.tanh)
def acc_ops_tanh(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.ActivationType.TANH
    return add_activation_layer(network, input_val, operation_type, name)
