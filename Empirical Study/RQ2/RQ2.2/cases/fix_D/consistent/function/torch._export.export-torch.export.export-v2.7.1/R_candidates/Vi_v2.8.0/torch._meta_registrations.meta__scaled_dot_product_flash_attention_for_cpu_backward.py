@register_meta(
    [
        aten._scaled_dot_product_flash_attention_for_cpu_backward,
    ]
)
def meta__scaled_dot_product_flash_attention_for_cpu_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    dropout_p: float,
    is_causal: bool,
    attn_mask: Optional[Tensor] = None,
    scale: Optional[float] = None,
):
    # cpus's grad layout is different from cuda's,
    # i.e. (batch_size, seq_len,num_heads, head_dim)
    batch_size = query.size(0)
    num_heads = query.size(1)
    head_dim = query.size(3)
    len_q = query.size(2)
    len_k = key.size(2)

    grad_q = torch.empty_permuted(
        (batch_size, num_heads, len_q, head_dim),
        (0, 2, 1, 3),
        dtype=query.dtype,
        device=query.device,
    )
    grad_k = torch.empty_permuted(
        (batch_size, num_heads, len_k, head_dim),
        (0, 2, 1, 3),
        dtype=key.dtype,
        device=key.device,
    )
    grad_v = torch.empty_permuted(
        (batch_size, num_heads, len_k, head_dim),
        (0, 2, 1, 3),
        dtype=value.dtype,
        device=value.device,
    )

    return grad_q, grad_k, grad_v
