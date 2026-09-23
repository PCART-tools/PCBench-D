def _xor_sum_aten(
    inp: TensorLikeType,
    dims: Optional[DimsSequenceType],
    *,
    dtype: Optional[torch.dtype] = None,
) -> Tensor:
    raise NotImplementedError("xor_sum only implemented with inductor")
