@register_decomposition_for_jvp(aten.batch_norm_backward)
def batch_norm_backward(
    grad_out: Tensor,
    input: Tensor,
    weight: Tensor,
    running_mean: Optional[Tensor],
    running_var: Optional[Tensor],
    save_mean: Optional[Tensor],
    save_var: Optional[Tensor],
    update: bool,
    eps: float,
    output_mask: list[bool],
    reserve: Tensor,
) -> tuple[Tensor, Optional[Tensor], Optional[Tensor]]:
    return native_batch_norm_backward(
        grad_out,
        input,
        weight,
        running_mean,
        running_var,
        save_mean,
        save_var,
        update,
        eps,
        output_mask,
    )
