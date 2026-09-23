def sample_inputs_spectral_ops(self, device, dtype, requires_grad=False, **kwargs):
    nd_tensor = partial(make_tensor, (S, S + 1, S + 2), device=device,
                        dtype=dtype, requires_grad=requires_grad)
    oned_tensor = partial(make_tensor, (31,), device=device,
                          dtype=dtype, requires_grad=requires_grad)

    if self.ndimensional == SpectralFuncType.ND:
        return [
            SampleInput(nd_tensor(),
                        kwargs=dict(s=(3, 10), dim=(1, 2), norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(s=(8,))),
            SampleInput(oned_tensor()),

            *(SampleInput(nd_tensor(),
                          kwargs=dict(dim=dim))
                for dim in [-1, -2, -3, (0, -1)]),
        ]
    elif self.ndimensional == SpectralFuncType.TwoD:
        return [
            SampleInput(nd_tensor(),
                        kwargs=dict(s=(3, 10), dim=(1, 2), norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(s=(6, 8))),
            SampleInput(nd_tensor(),
                        kwargs=dict(dim=0)),
            SampleInput(nd_tensor(),
                        kwargs=dict(dim=(0, -1))),
            SampleInput(nd_tensor(),
                        kwargs=dict(dim=(-3, -2, -1))),
        ]
    else:
        return [
            SampleInput(nd_tensor(),
                        kwargs=dict(n=10, dim=1, norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(norm='ortho')),
            SampleInput(nd_tensor(),
                        kwargs=dict(n=7)),
            SampleInput(oned_tensor()),

            *(SampleInput(nd_tensor(),
                          kwargs=dict(dim=dim))
                for dim in [-1, -2, -3]),
        ]
