@register_meta([aten._dyn_quant_matmul_4bit])
def meta__dyn_quant_matmul_4bit(
    inp,
    packed_weights,
    block_size,
    in_features,
    out_features,
):
    torch._check(inp.dim() == 2, lambda: "input must be a 2D tensor")
    torch._check(
        inp.dtype in [torch.float32],
        lambda: f"expected input to be f32, got {inp.dtype}",
    )
    M = inp.size(0)
    return inp.new_empty(M, out_features, dtype=inp.dtype)
