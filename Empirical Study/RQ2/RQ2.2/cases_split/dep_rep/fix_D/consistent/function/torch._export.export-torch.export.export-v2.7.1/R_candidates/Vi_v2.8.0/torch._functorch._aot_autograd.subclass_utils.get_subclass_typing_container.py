def get_subclass_typing_container(
    tensor_subclass: torch.Tensor,
) -> dict[type[torch.Tensor], list[type[torch.Tensor]]]:
    """
    Given a subclass, returns a recursive dictionary mapping each
    inner tensors to its' subclass types.
    """

    def _get_types_for_subclass(tensor_subclass: torch.Tensor) -> None:
        if not is_traceable_wrapper_subclass(tensor_subclass):
            return
        tracker[type(tensor_subclass)].append(tensor_subclass)
        inner_keys, _ = tensor_subclass.__tensor_flatten__()
        for key in inner_keys:
            inner_tensor = getattr(tensor_subclass, key)
            _get_types_for_subclass(inner_tensor)

    tracker: dict[Any, list[Any]] = collections.defaultdict(list)
    _get_types_for_subclass(tensor_subclass)
    return tracker
