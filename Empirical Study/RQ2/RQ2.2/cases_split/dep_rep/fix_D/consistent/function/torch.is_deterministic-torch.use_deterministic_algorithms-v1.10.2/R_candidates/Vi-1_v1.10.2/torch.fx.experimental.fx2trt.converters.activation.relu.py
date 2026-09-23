@tensorrt_converter(torch.nn.functional.relu)
@tensorrt_converter(torch.nn.modules.activation.ReLU)
def relu(network, submod, args, kwargs, layer_name):
    # args/kwargs should have already been normalized to kwargs
    assert len(args) == 0
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(f"ReLU received input {input_val} that is not part "
                           "of the TensorRT region!")

    def activation_dyn_range_fn(dyn_range):
        return max(0, dyn_range[0]), max(0, dyn_range[1])

    return common_activation(network, submod, input_val, trt.ActivationType.RELU, activation_dyn_range_fn, layer_name)
