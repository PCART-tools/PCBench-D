def _get_attr(model: torch.nn.Module, attr_name: str):
    return _get_attr_via_attr_list(model, attr_name.split("."))
