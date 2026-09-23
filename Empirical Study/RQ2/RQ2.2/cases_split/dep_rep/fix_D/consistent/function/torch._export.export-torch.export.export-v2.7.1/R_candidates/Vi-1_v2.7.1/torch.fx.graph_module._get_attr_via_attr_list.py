def _get_attr_via_attr_list(model: torch.nn.Module, attr_list: list[str]):
    if len(attr_list) == 0:
        return model
    *prefix, field = attr_list
    t = model
    for item in prefix:
        t = getattr(t, item, None)  # type: ignore[assignment]
        assert t is not None

    return getattr(t, field)
