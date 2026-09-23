@register_meta(
    [
        aten._scaled_dot_product_flash_attention_backward,
    ]
)
def meta__scaled_dot_product_flash_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    cum_seq_q: Tensor,
    cum_seq_k: Tensor,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    philox_seed: Tensor,
    philox_offset: Tensor,
    scale: Optional[float] = None,
):
    grad_q = torch.empty_like(query.transpose(1, 2)).transpose(1, 2)
    grad_k = torch.empty_like(key.transpose(1, 2)).transpose(1, 2)
    grad_v = torch.empty_like(value.transpose(1, 2)).transpose(1, 2)
    return grad_q, grad_k, grad_v
