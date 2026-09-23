def sample_inputs_where(op_info, device, dtype, requires_grad, **kwargs):
    for sample in sample_inputs_elementwise_njt_binary(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        other = sample.args[0]
        sample.args = ()
        sample.kwargs["other"] = other
        sample.kwargs["condition"] = sample.input > 0.0
        sample.name = sample.name.replace("(", "(NT, ")
        yield sample
