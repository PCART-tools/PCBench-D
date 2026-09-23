@_disable_dynamo_if_unsupported(single_tensor_fn=_single_tensor_adafactor)
def adafactor(
    params: list[Tensor],
    grads: list[Tensor],
    row_vars: list[Optional[Tensor]],
    col_vars: list[Optional[Tensor]],
    variances: list[Optional[Tensor]],
    state_steps: list[Tensor],
    # kwonly args with defaults are not supported by functions compiled with torchscript issue #70627
    # setting this as kwarg for now as functional API is compiled by torch/distributed/optim
    foreach: Optional[bool] = None,
    grad_scale: Optional[Tensor] = None,
    found_inf: Optional[Tensor] = None,
    has_complex: bool = False,
    *,
    d: float,
    lr: Union[float, Tensor],
    beta2_decay: float,
    weight_decay: float,
    eps1: float,
    eps2: float,
    maximize: bool,
):
    r"""Functional API that performs Adafactor algorithm computation.

    See :class:`~torch.optim.Adafactor` for details.
    """
    if not torch.compiler.is_compiling() and not all(
        isinstance(t, torch.Tensor) for t in state_steps
    ):
        raise RuntimeError(
            "`state_steps` argument must contain a list of singleton tensors"
        )

    if foreach:
        func = _multi_tensor_adafactor
    else:
        func = _single_tensor_adafactor

    func(
        params,
        grads,
        row_vars,
        col_vars,
        variances,
        state_steps,
        d=d,
        lr=lr,
        beta2_decay=beta2_decay,
        weight_decay=weight_decay,
        eps1=eps1,
        eps2=eps2,
        maximize=maximize,
        grad_scale=grad_scale,
        found_inf=found_inf,
        has_complex=has_complex,
    )
