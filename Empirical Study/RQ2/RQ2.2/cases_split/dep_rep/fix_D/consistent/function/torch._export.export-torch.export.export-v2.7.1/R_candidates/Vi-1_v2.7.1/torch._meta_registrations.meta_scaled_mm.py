@register_meta([aten._scaled_mm.default])
def meta_scaled_mm(
    self: torch.Tensor,
    mat2: torch.Tensor,
    scale_a: torch.Tensor,
    scale_b: torch.Tensor,
    bias: Optional[torch.Tensor] = None,
    scale_result: Optional[torch.Tensor] = None,
    out_dtype: Optional[torch.dtype] = None,
    use_fast_accum: bool = False,
):
    def is_fp8_type(dtype):
        return dtype in (
            torch.float8_e4m3fn,
            torch.float8_e5m2,
            torch.float8_e4m3fnuz,
            torch.float8_e5m2fnuz,
        )

    torch._check(
        self.dim() == 2 and mat2.dim() == 2,
        lambda: f"Inputs must be 2D but got self.dim()={self.dim()} and mat2.dim()={mat2.dim()}",
    )
    torch._check(
        is_fp8_type(self.dtype) and is_fp8_type(mat2.dtype),
        lambda: f"Expected both inputs to be fp8 types but got self.dtype={self.dtype} and mat2.dtype={mat2.dtype}",
    )

    if device_hint(self) == "cuda":

        def is_row_major(stride):
            return stride[0] > stride[1] and stride[1] == 1

        def is_col_major(stride):
            return stride[0] == 1 and stride[1] > 1

        def has_zero_dim(tensor_2d):
            return tensor_2d.size(0) == 0 or tensor_2d.size(1) == 0

        torch._check(
            is_row_major(self.stride()) or has_zero_dim(self),
            lambda: f"self must be row_major, got stride {self.stride()}",
        )
        torch._check(
            is_col_major(mat2.stride()) or has_zero_dim(mat2),
            lambda: f"mat2 must be col_major, got stride {mat2.stride()}",
        )
        torch._check(
            self.size(1) % 16 == 0,
            lambda: f"Expected self.size(1) to be divisible by 16, but got self.size(1)={self.size(1)}",
        )
        torch._check(
            mat2.size(0) % 16 == 0 and mat2.size(1) % 16 == 0,
            lambda: f"Expected both dimensions of mat2 to be divisble by 16 but got {mat2.shape}",
        )

        # determine scaling type and check input dimensions (refer to Blas.cpp op)
        torch._check(
            scale_a.dtype == torch.float32 and scale_b.dtype == torch.float32,
            lambda: "Both scale_a and scale_b must be float (fp32) tensors.",
        )
        m, _k = self.shape
        n = mat2.size(1)
        if scale_a.numel() == 1 and scale_b.numel() == 1:
            # tensorwise scaling
            pass
        else:
            # for non-tensorwise scaling, enforce 2D input tensors
            torch._check(
                scale_a.dim() == 2 and scale_b.dim() == 2,
                lambda: f"For non-tensorwise scaling, scale tensors must be 2D, but got {scale_a.dim()=} and {scale_b.dim()=}",
            )

            if (
                scale_a.size(0) == m
                and scale_a.size(1) == 1
                and scale_b.size(0) == 1
                and scale_b.size(1) == n
            ):
                # rowwise scaling
                torch._check(
                    scale_a.is_contiguous() and scale_b.is_contiguous(),
                    lambda: "Both scale_a and scale_b must be contiguous for rowwise scaling.",
                )
            else:
                # does not match any valid scaling type
                torch._check(
                    False,
                    lambda: (
                        "Invalid scaling configuration. "
                        "For tensorwise scaling, both scales should be scalar. "
                        f"For rowwise scaling, scale_a should be ({m}, 1), scale_b should be (1, {n}). "
                        f"Got scale_a.size()=({scale_a.size(0)}, {scale_a.size(1)}) "
                        f"and scale_b.size()=({scale_b.size(0)}, {scale_b.size(1)})"
                    ),
                )

    _out_dtype = out_dtype if out_dtype is not None else self.dtype
    return torch.empty(self.size(0), mat2.size(1), dtype=_out_dtype, device=self.device)
