@flex_attention.py_impl(FakeTensorMode)
def flex_attention_fake_tensor_mode(
    mode: FakeTensorMode,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    score_mod: Callable,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple = (),
    mask_mod_other_buffers: tuple = (),
) -> tuple[torch.Tensor, torch.Tensor]:
    with mode:
        out, logsumexp = flex_attention_fake_impl(query, value)
        return out, logsumexp
