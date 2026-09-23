@register_flop_formula([aten._scaled_dot_product_efficient_attention_backward,
                        aten._scaled_dot_product_flash_attention_backward,
                        aten._scaled_dot_product_cudnn_attention_backward])
def sdpa_backward_flop(grad_out_shape, query_shape, key_shape, value_shape, *args, out_shape=None, **kwargs) -> int:
    """Count flops for self-attention backward."""
    return sdpa_backward_flop_count(grad_out_shape, query_shape, key_shape, value_shape)
