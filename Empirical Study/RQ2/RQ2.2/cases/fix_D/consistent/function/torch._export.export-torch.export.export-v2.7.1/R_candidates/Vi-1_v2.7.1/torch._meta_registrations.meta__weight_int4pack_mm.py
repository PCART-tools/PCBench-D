@register_meta([aten._weight_int4pack_mm])
def meta__weight_int4pack_mm(x, w, q_group_size, q_scale_and_zeros):
    torch._check(x.dim() == 2, lambda: "x must be a 2D tensor")
    torch._check(w.dim() == 4, lambda: "w must be a 4D tensor")
    torch._check(
        x.dtype in [torch.float32, torch.float16, torch.bfloat16],
        lambda: f"expected x to be f32/f16/bf16, got {x.dtype}",
    )
    torch._check(
        w.dtype is torch.int32,
        lambda: f"expected w to be int32, got {w.dtype}",
    )
    return x.new_empty(x.size(0), w.size(0) * 8, dtype=x.dtype)
