def flex_attention_fake_impl(
    query: torch.Tensor, value: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
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
