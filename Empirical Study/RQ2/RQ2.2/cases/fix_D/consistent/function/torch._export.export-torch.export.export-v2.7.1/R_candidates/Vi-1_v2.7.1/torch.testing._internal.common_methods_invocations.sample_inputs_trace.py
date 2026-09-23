def sample_inputs_trace(self, device, dtype, requires_grad, **kwargs):
    yield SampleInput(
        make_tensor((S, S), dtype=dtype, device=device,
                    low=None, high=None,
                    requires_grad=requires_grad))
