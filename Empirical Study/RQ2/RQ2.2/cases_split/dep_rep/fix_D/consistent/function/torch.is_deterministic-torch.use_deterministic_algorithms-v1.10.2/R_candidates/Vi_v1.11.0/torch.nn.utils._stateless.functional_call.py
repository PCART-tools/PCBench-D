def functional_call(
    module: torch.nn.Module,
    parameters_and_buffers: Dict[str, Tensor],
    args: Tuple,
    kwargs : Dict[str, Any] = None,
):
    r"""Performs a functional call on the module by replacing the module parameters
    and buffers with the provided ones.

    .. note:: If the module has active parametrizations, passing a value in the
        `parameters_and_buffers` argument with the name set to the regular parameter
         name will completely disable the parametrization.
         If you want to apply the parametrization function to the value passed
         please set the key as `{submodule_name}.parametrizations.{parameter_name}.original`.

    Args:
        module (torch.nn.Module): the module to call
        parameters_and_buffers (dict of str and Tensor): the parameters that will be used in
            the module call.
        args (tuple): arguments to be passed to the module call
        kwargs (dict): keyword arguments to be passed to the module call

    Returns:
        Any: the result of calling ``module``.
    """
    # TODO allow kwargs such as unsafe and others for parametrization
    if (
            torch.jit.is_tracing()
            or torch.jit.is_scripting()
            or isinstance(module, (
                torch.jit.RecursiveScriptModule,
                torch.jit.ScriptModule,
                torch.jit.ScriptFunction)
            )
    ):
        raise RuntimeError("The stateless API can't be used with Jitted modules")
    if kwargs is None:
        kwargs = {}
    with reparametrize_module(module, parameters_and_buffers):
        if isinstance(args, tuple):
            out = module(*args, **kwargs)
        else:
            out = module(args, **kwargs)
    return out
