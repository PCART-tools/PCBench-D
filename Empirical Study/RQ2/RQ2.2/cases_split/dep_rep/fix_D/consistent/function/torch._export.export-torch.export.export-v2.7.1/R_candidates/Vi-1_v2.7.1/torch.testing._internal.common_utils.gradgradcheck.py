def gradgradcheck(fn, inputs, grad_outputs=None, **kwargs):
    # Wrapper around gradgradcheck that enables certain keys by default
    # See gradcheck above for an explanation of why we need something like this.
    #
    # All PyTorch devs doing testing should use this wrapper instead of autograd.gradgradcheck
    default_values = {
        "check_batched_grad": True,
        "fast_mode": True,
    }

    if TEST_WITH_SLOW_GRADCHECK:
        default_values["fast_mode"] = False

    for key, value in default_values.items():
        # default value override values explicitly set to None
        k = kwargs.get(key, None)
        kwargs[key] = k if k is not None else value

    return torch.autograd.gradgradcheck(fn, inputs, grad_outputs, **kwargs)
