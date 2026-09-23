@register_decomposition(aten._batch_norm_with_update_functional.default)
def _batch_norm_with_update_functional(
    input: Tensor,
    weight: Optional[Tensor],
    bias: Optional[Tensor],
    running_mean: Tensor,
    running_var: Tensor,
    momentum: float,
    eps: float,
) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    (
        output,
        save_mean,
        save_rstd,
        new_rm,
        new_rv,
    ) = native_batch_norm_helper(
        input, weight, bias, running_mean, running_var, True, momentum, eps, True
    )
    reserve = _get_batch_norm_reserve_tensor(
        input, weight, bias, running_mean, running_var, eps, training=True
    )
    assert new_rm is not None, "new_running_mean should not be None"
    assert new_rv is not None, "new_running_var should not be None"
    return (output, save_mean, save_rstd, reserve, new_rm, new_rv)
