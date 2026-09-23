def get_task_func(task: str) -> Callable:
    def hessian_fwdrev(model, inp, strict=None):
        return functional.hessian(model, inp, strict=False, vectorize=True, outer_jacobian_strategy="forward-mode")

    def hessian_revrev(model, inp, strict=None):
        return functional.hessian(model, inp, strict=False, vectorize=True)

    def jacfwd(model, inp, strict=None):
        return functional.jacobian(model, inp, strict=False, vectorize=True, strategy="forward-mode")

    def jacrev(model, inp, strict=None):
        return functional.jacobian(model, inp, strict=False, vectorize=True)

    if task == "hessian_fwdrev":
        return hessian_fwdrev
    elif task == "hessian_revrev":
        return hessian_revrev
    elif task == "jacfwd":
        return jacfwd
    elif task == "jacrev":
        return jacrev
    else:
        return getattr(functional, task)
