def _integral_bound(f, a, b, step, args, constants):
    # Estimate the sum with integral approximation
    dtype, log, _, _, rtol, atol, maxterms = constants
    log2 = np.log(2, dtype=dtype)

    # Get a lower bound on the sum and compute effective absolute tolerance
    lb = _tanhsinh(f, a, b, args=args, atol=atol, rtol=rtol, log=log)
    tol = np.broadcast_to(atol, lb.integral.shape)
    tol = _logsumexp((tol, rtol + lb.integral)) if log else tol + rtol*lb.integral
    i_skip = lb.status < 0  # avoid unnecessary f_evals if integral is divergent
    tol[i_skip] = np.nan
    status = lb.status

    # As in `_direct`, we'll need a temporary new axis for points
    # at which to evaluate the function. Append axis at the end for
    # consistency with other elementwise algorithms.
    a2 = a[..., np.newaxis]
    step2 = step[..., np.newaxis]
    args2 = [arg[..., np.newaxis] for arg in args]

    # Find the location of a term that is less than the tolerance (if possible)
    log2maxterms = np.floor(np.log2(maxterms)) if maxterms else 0
    n_steps = np.concatenate([2**np.arange(0, log2maxterms), [maxterms]], dtype=dtype)
    nfev = len(n_steps)
    ks = a2 + n_steps * step2
    fks = f(ks, *args2)
    nt = np.minimum(np.sum(fks > tol[:, np.newaxis], axis=-1),  n_steps.shape[-1]-1)
    n_steps = n_steps[nt]

    # Directly evaluate the sum up to this term
    k = a + n_steps * step
    left, left_error, left_nfev = _direct(f, a, k, step, args,
                                          constants, inclusive=False)
    i_skip |= np.isposinf(left)  # if sum is not finite, no sense in continuing
    status[np.isposinf(left)] = -3
    k[i_skip] = np.nan

    # Use integration to estimate the remaining sum
    # Possible optimization for future work: if there were no terms less than
    # the tolerance, there is no need to compute the integral to better accuracy.
    # Something like:
    # atol = np.maximum(atol, np.minimum(fk/2 - fb/2))
    # rtol = np.maximum(rtol, np.minimum((fk/2 - fb/2)/left))
    # where `fk`/`fb` are currently calculated below.
    right = _tanhsinh(f, k, b, args=args, atol=atol, rtol=rtol, log=log)

    # Calculate the full estimate and error from the pieces
    fk = fks[np.arange(len(fks)), nt]
    fb = f(b, *args)
    nfev += 1
    if log:
        log_step = np.log(step)
        S_terms = (left, right.integral - log_step, fk - log2, fb - log2)
        S = _logsumexp(S_terms, axis=0)
        E_terms = (left_error, right.error - log_step, fk-log2, fb-log2+np.pi*1j)
        E = _logsumexp(E_terms, axis=0).real
    else:
        S = left + right.integral/step + fk/2 + fb/2
        E = left_error + right.error/step + fk/2 - fb/2
    status[~i_skip] = right.status[~i_skip]
    return S, E, status, left_nfev + right.nfev + nfev + lb.nfev
