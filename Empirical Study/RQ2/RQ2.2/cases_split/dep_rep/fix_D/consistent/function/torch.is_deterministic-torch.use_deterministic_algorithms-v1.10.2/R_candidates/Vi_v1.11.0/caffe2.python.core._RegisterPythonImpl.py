def _RegisterPythonImpl(
    f, grad_f=None, python_func_type=None, pass_workspace=False
):
    if python_func_type:
        func = python_func_type(f)
        f = func.forward
        grad_f = func.backward
    else:
        if isinstance(f, tuple):
            f = f[0](*f[1], **f[2])
        if isinstance(grad_f, tuple):
            grad_f = grad_f[0](*grad_f[1], **grad_f[2])

    token = C.register_python_op(f, pass_workspace, '')
    if grad_f:
        C.register_python_gradient_op(token, grad_f)
    return token
