def sample_inputs_new_full(self, device, dtype, requires_grad, **kwargs):
    def get_val(dtype):
        return make_tensor([], 'cpu', dtype).item()

    samples = []
    for sample in sample_inputs_new_fns(self, device, dtype, requires_grad, **kwargs):
        # The scalar we are passing to new_full must be the same dtype
        # as the one of the resulting tensor
        use_dtype = sample.kwargs['dtype'] if 'dtype' in sample.kwargs else dtype
        samples.append(SampleInput(
            sample.input, args=sample.args + (get_val(use_dtype),), kwargs=sample.kwargs))
    return tuple(samples)
