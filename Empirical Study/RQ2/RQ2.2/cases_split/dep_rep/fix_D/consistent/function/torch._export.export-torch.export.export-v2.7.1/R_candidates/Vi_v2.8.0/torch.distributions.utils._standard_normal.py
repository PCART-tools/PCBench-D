def _standard_normal(
    shape: Sequence[Union[int, SymInt]],
    dtype: Optional[_dtype],
    device: Optional[Device],
) -> Tensor:
    if torch._C._get_tracing_state():
        # [JIT WORKAROUND] lack of support for .normal_()
        return torch.normal(
            torch.zeros(shape, dtype=dtype, device=device),
            torch.ones(shape, dtype=dtype, device=device),
        )
    return torch.empty(shape, dtype=dtype, device=device).normal_()
