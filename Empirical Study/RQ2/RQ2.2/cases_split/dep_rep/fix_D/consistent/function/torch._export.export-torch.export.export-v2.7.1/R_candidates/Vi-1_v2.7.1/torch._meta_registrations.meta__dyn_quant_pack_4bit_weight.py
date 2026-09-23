@register_meta([aten._dyn_quant_pack_4bit_weight])
def meta__dyn_quant_pack_4bit_weight(
    weights, scales_zeros, bias: Optional[Tensor], block_size, in_features, out_features
):
    torch._check(
        weights.dtype is torch.uint8,
        lambda: f"expected w to be uint8, got {weights.dtype}",
    )
    if torch.backends.kleidiai.is_available() and (
        (block_size == in_features and scales_zeros.dtype == torch.float)
        or (
            block_size < in_features
            and block_size % 32 == 0
            and in_features % block_size == 0
            and scales_zeros.dtype == torch.bfloat16
        )
    ):
        packed_weight_size = get_kai_packed_weight_size(
            4, out_features, in_features, block_size
        )
        return weights.new_empty(int(packed_weight_size), dtype=torch.uint8)
    packed_weight_size = weights.numel() + scales_zeros.numel()
    return weights.new_empty(packed_weight_size, dtype=torch.float)
