def CreatePythonOperator(
    f, inputs,
    outputs,
    grad_f=None,
    pass_workspace=False,
    python_func_type=None,
    *args,
    **kwargs
):
    """
    `f` should have a signature (inputs, outputs)

    If `pass_workspace` is True, the signature is changed to
    (inputs, outputs, workspace) where `workspace` is the workspace the op
    is going to run on. This is potentially dangerous (as the op can manipulate
    the workspace directly), use on your own risk.
    """
    kwargs["token"] = _RegisterPythonImpl(
        f, grad_f, python_func_type, pass_workspace=pass_workspace
    )
    return CreateOperator("Python", inputs, outputs, *args, **kwargs)
