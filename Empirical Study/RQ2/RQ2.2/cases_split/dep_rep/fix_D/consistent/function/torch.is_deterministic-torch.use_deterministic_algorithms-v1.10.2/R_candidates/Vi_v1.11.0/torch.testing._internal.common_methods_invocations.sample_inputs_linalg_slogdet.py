def sample_inputs_linalg_slogdet(op_info, device, dtype, requires_grad=False, **kwargs):
    def out_fn(output):
        return output[1]

    samples = sample_inputs_linalg_invertible(op_info, device, dtype, requires_grad)
    for sample in samples:
        sample.output_process_fn_grad = out_fn
        yield sample
