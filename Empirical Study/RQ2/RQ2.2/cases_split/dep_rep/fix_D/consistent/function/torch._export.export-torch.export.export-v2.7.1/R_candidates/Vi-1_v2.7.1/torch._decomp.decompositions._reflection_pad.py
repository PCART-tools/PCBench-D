@register_decomposition(aten.reflection_pad1d)
@register_decomposition(aten.reflection_pad2d)
@register_decomposition(aten.reflection_pad3d)
@pw_cast_for_opmath
@out_wrapper()
def _reflection_pad(a: Tensor, padding: tuple[int, ...]) -> Tensor:
    def idx(left, middle, right):
        dim_idx = torch.arange(-left, middle + right, device=a.device)
        return middle - 1 - (middle - 1 - dim_idx.abs()).abs()

    return _reflection_or_replication_pad(
        a,
        padding,
        idx,
    )
