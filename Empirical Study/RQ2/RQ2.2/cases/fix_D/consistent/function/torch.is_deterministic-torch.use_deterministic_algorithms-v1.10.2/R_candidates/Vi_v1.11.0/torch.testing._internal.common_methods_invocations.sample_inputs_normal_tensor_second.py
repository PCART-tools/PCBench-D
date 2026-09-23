def sample_inputs_normal_tensor_second(self, device, dtype, requires_grad, **kwargs):
    cases = [
        ([3, 4], 0.3, {}),
    ]
    return sample_inputs_normal_common(self, device, dtype, requires_grad, cases, **kwargs)
