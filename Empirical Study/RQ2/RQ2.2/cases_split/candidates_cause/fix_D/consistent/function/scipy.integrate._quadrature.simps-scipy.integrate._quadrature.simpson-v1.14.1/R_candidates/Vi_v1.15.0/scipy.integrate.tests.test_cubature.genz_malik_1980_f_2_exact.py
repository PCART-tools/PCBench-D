def genz_malik_1980_f_2_exact(a, b, alphas, betas, xp):
    ndim = xp_size(a)
    a = xp.reshape(a, (*([1]*(len(alphas.shape) - 1)), ndim))
    b = xp.reshape(b, (*([1]*(len(alphas.shape) - 1)), ndim))

    # `xp` is the unwrapped namespace, so `.atan` won't work for `xp = np` and np<2.
    xp_test = array_namespace(a)

    return (
        (-1)**ndim * 1/xp.prod(alphas, axis=-1)
        * xp.prod(
            xp_test.atan((a - betas)/alphas) - xp_test.atan((b - betas)/alphas),
            axis=-1,
        )
    )
