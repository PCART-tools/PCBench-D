@register_decomposition(aten._native_batch_norm_legit_functional.default)
def _native_batch_norm_legit_functional(
    input: Tensor,
    weight: Optional[Tensor],
    bias: Optional[Tensor],
    running_mean: Tensor,
    running_var: Tensor,
    training: bool,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    (
        output,
        save_mean,
        save_rstd,
        new_running_mean,
        new_running_var,
    ) = native_batch_norm_helper(
        input, weight, bias, running_mean, running_var, training, momentum, eps, True
    )
    assert new_running_mean is not None, "new_running_mean should not be None"
    assert new_running_var is not None, "new_running_var should not be None"
    return output, save_mean, save_rstd, new_running_mean, new_running_var
