def _get_rand_no_zeros(*args, **kwargs):
    requires_grad = kwargs.get('requires_grad', False)
    kwargs_without_requires_grad = kwargs.copy()
    kwargs_without_requires_grad['requires_grad'] = False
    result = torch.rand(*args, **kwargs_without_requires_grad)
    return result.clamp_min_(0.1).requires_grad_(requires_grad)
