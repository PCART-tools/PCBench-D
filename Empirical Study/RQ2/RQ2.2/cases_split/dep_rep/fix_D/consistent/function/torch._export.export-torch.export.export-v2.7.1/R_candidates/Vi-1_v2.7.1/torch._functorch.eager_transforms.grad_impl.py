def grad_impl(func: Callable, argnums: argnums_t, has_aux: bool, args, kwargs):
    results = grad_and_value_impl(func, argnums, has_aux, args, kwargs)
    if has_aux:
        grad, (_, aux) = results
        return grad, aux
    grad, _ = results
    return grad
