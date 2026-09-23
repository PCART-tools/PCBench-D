    @register_meta(torch.ops.quantized.int4mm_packed_weight_cpu)
    def meta_int4mm_packed_weight_cpu(x, w, q_group_size, q_scale_and_zeros):
        torch._check(x.dim() == 2, f"x must be a 2D tensor, got {x.dim()}D")
        torch._check(w.dim() == 2, f"w must be a 2D tensor, got {w.dim()}D")
        torch._check(
            x.dtype in [torch.float32, torch.float16, torch.bfloat16],
            f"expected x to be f32/f16/bf16, got {x.dtype}",
        )
        torch._check(w.dtype == torch.uint8, f"expected w to be uint8, got {w.dtype}")
        torch._check(
            q_group_size.dtype == torch.int64,
            f"q_group_size must be int64, got {q_group_size.dtype}",
        )
        torch._check(
            q_scale_and_zeros.dtype == x.dtype,
            f"q_scale_and_zeros must have the same dtype as x, got {q_scale_and_zeros.dtype}",
        )
        return x.new_empty(x.size(0), w.size(0), dtype=x.dtype)
