@register_decomposition([aten.empty_permuted.default])
def empty_permuted(
    size: list[Union[int, torch.SymInt]],
    physical_layout: list[int],
    **kwargs: Any,
) -> torch.Tensor:
    perm = [0] * len(size)
    for p, l in enumerate(physical_layout):
        perm[l] = p
    return torch.empty([size[l] for l in physical_layout], **kwargs).permute(perm)
