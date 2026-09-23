def doesnt_support_saved_tensors_hooks(f):
    message = (
        "torch.func.{grad, vjp, jacrev, hessian} don't yet support saved tensor hooks. "
        "Please open an issue with your use case."
    )

    @functools.wraps(f)
    def fn(*args, **kwargs):
        with torch.autograd.graph.disable_saved_tensors_hooks(message):
            return f(*args, **kwargs)

    return fn
