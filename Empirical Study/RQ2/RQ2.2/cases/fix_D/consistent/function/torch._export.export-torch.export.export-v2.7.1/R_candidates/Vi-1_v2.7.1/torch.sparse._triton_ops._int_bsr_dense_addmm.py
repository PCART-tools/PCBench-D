def _int_bsr_dense_addmm(
    input: torch.Tensor,
    bsr: torch.Tensor,
    dense: torch.Tensor,
    *,
    beta=1,
    alpha=1,
    left_alpha: Optional[torch.Tensor] = None,
    right_alpha: Optional[torch.Tensor] = None,
    out: Optional[torch.Tensor] = None,
    skip_checks: bool = False,
    max_grid: Optional[tuple[Optional[int], Optional[int], Optional[int]]] = None,
    meta: Optional[dict] = None,
):
    if out is None and dense.dtype is torch.int8:
        f_name = "_int_bsr_dense_addmm"
        crow_indices = bsr.crow_indices()
        batch_ndim = crow_indices.dim() - 1
        M = bsr.shape[batch_ndim]
        N = dense.shape[-1]
        original_batch_dims_broadcasted = broadcast_batch_dims(f_name, bsr, dense)
        out = torch.empty(
            original_batch_dims_broadcasted + (M, N),
            dtype=torch.int32,
            device=dense.device,
        )
    return bsr_dense_addmm(
        input,
        bsr,
        dense,
        beta=beta,
        alpha=alpha,
        left_alpha=left_alpha,
        right_alpha=right_alpha,
        out=out,
        skip_checks=skip_checks,
        max_grid=max_grid,
        meta=meta,
    )
