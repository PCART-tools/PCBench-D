@register_fake(flex_attention)
def flex_attention_fake_impl(
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
    if has_user_subclass(
        (
            query,
            key,
            value,
            score_mod,
            block_mask,
            scale,
            kernel_options,
            score_mod_other_buffers,
            mask_mod_other_buffers,
        ),
        allowed_subclasses=(FakeTensor,),
    ):
        return NotImplemented

    # TODO: Figure out a better way to handle this for NJT than using sum()
    if query.is_nested:
        out = torch.empty_like(query, memory_format=torch.contiguous_format)
        logsumexp = query.sum(dim=-1)
        return out, logsumexp

    v_head_dim = value.size(-1)
    batch_size, num_heads, seq_len_q, _q_head_dim = query.shape
    logsumexp = query.new_empty(batch_size, num_heads, seq_len_q, dtype=torch.float32)
    out_shape = (batch_size, num_heads, seq_len_q, v_head_dim)
    out = query.new_empty(out_shape)
    out = _permute_strides(out, query.stride())
    return out, logsumexp
