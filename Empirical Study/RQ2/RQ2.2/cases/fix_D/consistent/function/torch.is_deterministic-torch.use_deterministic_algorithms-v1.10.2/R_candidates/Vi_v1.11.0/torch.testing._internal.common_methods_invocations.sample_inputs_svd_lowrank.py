def sample_inputs_svd_lowrank(op_info, device, dtype, requires_grad=False, **kwargs):
    for sample in sample_inputs_singular_matrix_factors(op_info, device, dtype, requires_grad, **kwargs):
        *batch, m, k = sample.input.shape
        *_, n, _ = sample.args[0].shape

        # NOTE: since svd_lowrank relies on non rank-revealing SVD,
        # it inherits the problem of unstable behavior with repeated
        # singular values including zeros.
        # Since we want to avoid (repeated) zeros as singular values,
        # we can only use k for q.
        # This issues could be resolved with using a rank-revealing SVD
        # which does not include "zero" singular values.
        op_kwargs = {
            'q': k,
            'M': None
        }

        # without M specified
        yield clone_sample(sample, **op_kwargs)

        # now with M
        # TODO: fix bug in the documentation for svd_lowrank:
        # M has to be (*, m, n), and not (*, 1, n) as written
        # in the documentation
        op_kwargs['M'] = make_tensor((*batch, m, n), device, dtype, requires_grad=requires_grad)
        yield clone_sample(sample, **op_kwargs)
