def sample_inputs_spectral_ops(self, device, dtype, requires_grad=False, **kwargs):
    nd_tensor = make_tensor((S, S + 1, S + 2), device, dtype, low=None, high=None,
                            requires_grad=requires_grad)
    tensor = make_tensor((31,), device, dtype, low=None, high=None,
                         requires_grad=requires_grad)

    if self.ndimensional:
        return [
            SampleInput(nd_tensor, kwargs=dict(s=(3, 10), dim=(1, 2), norm='ortho')),
            SampleInput(nd_tensor, kwargs=dict(norm='ortho')),
            SampleInput(nd_tensor, kwargs=dict(s=(8,))),
            SampleInput(tensor),

            *(SampleInput(nd_tensor, kwargs=dict(dim=dim))
                for dim in [-1, -2, -3, (0, -1)]),
        ]
    else:
        return [
            SampleInput(nd_tensor, kwargs=dict(n=10, dim=1, norm='ortho')),
            SampleInput(nd_tensor, kwargs=dict(norm='ortho')),
            SampleInput(nd_tensor, kwargs=dict(n=7)),
            SampleInput(tensor),

            *(SampleInput(nd_tensor, kwargs=dict(dim=dim))
                for dim in [-1, -2, -3]),
        ]
