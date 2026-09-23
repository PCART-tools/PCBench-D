@register_meta([aten._scaled_dot_product_fused_attention_overrideable])
def meta__scaled_dot_product_fused_attention_overrideable(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    attn_bias: Optional[Tensor] = None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    scale: Optional[float] = None,
):
    B = query.size(0)
    H = query.size(1)
    S_Q = query.size(2)
    S_KV = key.size(2)
    D_V = value.size(-1)

    res = torch.empty((B, H, S_Q, D_V), dtype=query.dtype, device=query.device)
    logsum_exp = torch.empty(
        (B, H, S_Q),
        dtype=torch.float,
        device=query.device,
    )

    # See Note [Seed and Offset]
    seed = torch.empty((), dtype=torch.long, device="meta")
    offset = torch.empty((), dtype=torch.long, device="meta")

    return (
        res,
        logsum_exp,
        None,
        None,
        S_Q,
        S_KV,
        seed,
        offset,
        None,
    )
