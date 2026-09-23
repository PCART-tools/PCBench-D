@register_decomposition([aten.full])
def full(
    size: list[Union[int, torch.SymInt]],
    fill_value: torch.types.Number,
    **kwargs: Any,
) -> torch.Tensor:
    dtype = kwargs.get("dtype")
    if dtype is None:
        kwargs["dtype"] = type_to_dtype(type(fill_value))
        return torch.full(size, fill_value, **kwargs)
    return NotImplemented
