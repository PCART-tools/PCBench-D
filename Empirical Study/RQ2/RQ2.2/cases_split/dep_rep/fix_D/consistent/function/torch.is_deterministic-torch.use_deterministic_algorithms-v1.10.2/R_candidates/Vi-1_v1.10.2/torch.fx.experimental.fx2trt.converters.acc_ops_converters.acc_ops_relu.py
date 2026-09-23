@tensorrt_converter(acc_ops.relu)
def acc_ops_relu(network, target, args, kwargs, name):
    input_val = kwargs["input"]
    operation_type = trt.ActivationType.RELU
    return add_activation_layer(network, input_val, operation_type, name)
