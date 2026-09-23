@register_decomposition(
    [aten.split_with_sizes_copy.default, aten.split_with_sizes_copy.out]
)
def split_with_sizes_copy(
    self: Tensor,
    split_sizes: list[int],
    dim: int = 0,
    out: Optional[list[Tensor]] = None,
) -> Optional[list[Tensor]]:
    splits = aten.split_with_sizes(self, split_sizes, dim=dim)
    if out is None:
        return [s.clone(memory_format=torch.contiguous_format) for s in splits]
    else:
        for output, split in zip(out, splits):
            _maybe_resize_out(output, split.shape)
            _safe_copy_out(copy_from=split, copy_to=output, exact_dtype=True)
        return None
