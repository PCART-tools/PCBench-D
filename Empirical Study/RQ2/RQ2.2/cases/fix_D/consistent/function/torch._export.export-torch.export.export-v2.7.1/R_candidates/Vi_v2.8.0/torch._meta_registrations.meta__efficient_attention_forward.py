@register_meta(
    [
        aten._efficient_attention_forward,
    ]
)
def meta__efficient_attention_forward(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    bias: Optional[Tensor],
    cu_seqlens_q: Optional[Tensor],
    cu_seqlens_k: Optional[Tensor],
    max_seqlen_q: Optional[int],
    max_seqlen_k: Optional[int],
    dropout_p: float,
    custom_mask_type: int,
    compute_log_sumexp: bool = False,
    scale: Optional[float] = None,
    causal_diagonal: Optional[Tensor] = None,
    seqlen_k: Optional[Tensor] = None,
    window_size: Optional[int] = None,
):
    B = query.size(0)
    M = query.size(1)
    N = key.size(1)
    num_heads = query.size(-2)
    Kv = value.size(-1)

    res = torch.empty(B, M, num_heads, Kv, dtype=query.dtype, device=query.device)

    logsumexp_batch_dim = cu_seqlens_q.size(0) - 1 if (cu_seqlens_q is not None) else B
    actual_max_seqlen_q = M
    if cu_seqlens_q is not None:
        assert max_seqlen_q is not None
        actual_max_seqlen_q = max_seqlen_q
    actual_max_seqlen_k = max_seqlen_k if max_seqlen_k is not None else N
    logsumexp_dim = (
        math.ceil(actual_max_seqlen_q / 32) * 32 if compute_log_sumexp else 0
    )
    logsum_exp = torch.empty(
        (logsumexp_batch_dim, num_heads, logsumexp_dim),
        dtype=torch.float,
        device=query.device,
    )

    # See Note [Seed and Offset]:
    seed = torch.empty((), dtype=torch.long, device="meta")
    offset = torch.empty((), dtype=torch.long, device="meta")

    return res, logsum_exp, seed, offset, actual_max_seqlen_q, actual_max_seqlen_k
