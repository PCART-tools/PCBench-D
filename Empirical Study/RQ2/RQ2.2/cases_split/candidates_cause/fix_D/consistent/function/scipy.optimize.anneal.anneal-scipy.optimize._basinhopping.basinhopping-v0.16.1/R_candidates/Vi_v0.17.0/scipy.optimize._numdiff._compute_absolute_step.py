def _compute_absolute_step(rel_step, x0, method):
    if rel_step is None:
        if method == '2-point':
            rel_step = EPS**0.5
        elif method == '3-point':
            rel_step = EPS**(1 / 3)
        elif method == 'cs':
            rel_step = EPS**(0.5)
        else:
            raise ValueError("`method` must be '2-point' or '3-point'.")

    sign_x0 = (x0 >= 0).astype(float) * 2 - 1
    return rel_step * sign_x0 * np.maximum(1.0, np.abs(x0))
