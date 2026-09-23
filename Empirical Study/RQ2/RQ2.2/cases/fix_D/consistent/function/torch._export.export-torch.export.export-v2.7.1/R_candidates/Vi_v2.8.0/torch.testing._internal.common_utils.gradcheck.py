def gradcheck(fn, inputs, **kwargs):
    # Wrapper around gradcheck that enables certain keys by default.
    # Use this testing-internal gradcheck instead of autograd.gradcheck so that new features like vmap and
    # forward-mode AD are tested by default. We create this wrapper because we'd like to keep new checks
    # to be disabled to default for the public-facing api to avoid breaking user code.
    #
    # All PyTorch devs doing testing should use this wrapper instead of autograd.gradcheck.
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

    return torch.autograd.gradcheck(fn, inputs, **kwargs)
