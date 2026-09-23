    def bsr_dense_mm(
        bsr: torch.Tensor,
        dense: torch.Tensor,
        *,
        out: Optional[torch.Tensor] = None,
        skip_checks: bool = False,
        max_grid: Optional[tuple[Optional[int], Optional[int], Optional[int]]] = None,
        meta: Optional[dict] = None,
    ):
        f_name = "bsr_dense_mm"
        m, _kl = bsr.shape[-2:]
        if not skip_checks:
            check_bsr_layout(f_name, bsr)
            check_device(f_name, bsr, dense.device)
            check_dtype(f_name, bsr, dense.dtype, (torch.int8,))
            check_mm_compatible_shapes(f_name, bsr, dense)

            n = dense.size(-1)
            row_block, col_block = bsr.values().shape[-2:]
            check_blocksize(f_name, (row_block, col_block))
            check(
                not n % 16,
                f"{f_name}(): dense.size(-1) == {n} should be divisible by 16",
            )
        else:
            _kr, n = dense.shape[-2:]

        original_batch_dims_broadcasted = broadcast_batch_dims(f_name, bsr, dense)

        if out is not None and not skip_checks:
            expected_out_shape = original_batch_dims_broadcasted + (m, n)
            check(
                out.shape == expected_out_shape,
                "bsr_dense_mm(): `out` argument has wrong shape, "
                f"expected {expected_out_shape}, but got {out.shape}.",
            )
            check(
                out.is_contiguous() or out.transpose(-2, -1).is_contiguous(),
                "bsr_dense_mm(): only row-major/col-major `out` arguments are supported, "
                "i.e. (out.is_contiguous() or out.transpose(-2, -1).is_contiguous()) "
                "should be True.",
            )

        # Allocate out
        if out is None:
            out = dense.new_empty(original_batch_dims_broadcasted + (m, n))

        # Short circuit if lhs is zero
        if bsr._nnz() == 0:
            return out.zero_()

        # with beta==0, addmm ignores input content, so we can use out
        # as a placeholder for input because their shapes match:
        return bsr_dense_addmm(out, bsr, dense, alpha=1, beta=0, out=out)
