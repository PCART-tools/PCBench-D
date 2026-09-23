@register_decomposition([aten.view_copy.default])
def view_copy_default(
    self: torch.Tensor,
    size: list[Union[int, torch.SymInt]],
) -> torch.Tensor:
    return aten.view(self, size).clone()
