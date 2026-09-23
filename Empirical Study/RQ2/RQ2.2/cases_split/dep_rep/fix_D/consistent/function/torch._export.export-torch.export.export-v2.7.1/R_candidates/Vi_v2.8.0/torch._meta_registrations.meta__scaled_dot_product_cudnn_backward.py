@register_meta(
    [
        aten._scaled_dot_product_cudnn_attention_backward,
    ]
)
def meta__scaled_dot_product_cudnn_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    out: Tensor,
    logsumexp: Tensor,
    philox_seed: Tensor,
    philox_offset: Tensor,
    attn_bias: Tensor,
    cum_seq_q: Tensor,
    cum_seq_k: Tensor,
    max_q: int,
    max_k: int,
    dropout_p: float,
    is_causal: bool,
    scale: Optional[float] = None,
):
    grad_q = torch.empty_like(query)
    grad_k = torch.empty_like(key)
    grad_v = torch.empty_like(value)
    return grad_q, grad_k, grad_v
