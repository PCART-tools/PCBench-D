@register_flop_formula([aten._scaled_dot_product_efficient_attention,
                        aten._scaled_dot_product_flash_attention,
                        aten._scaled_dot_product_cudnn_attention])
def sdpa_flop(query_shape, key_shape, value_shape, *args, out_shape=None, **kwargs) -> int:
    """Count flops for self-attention."""
    # NB: We aren't accounting for causal attention here
    return sdpa_flop_count(query_shape, key_shape, value_shape)
