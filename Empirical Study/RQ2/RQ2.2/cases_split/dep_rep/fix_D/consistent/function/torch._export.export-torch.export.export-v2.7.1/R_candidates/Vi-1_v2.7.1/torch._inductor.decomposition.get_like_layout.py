def get_like_layout(
    tensor: torch.Tensor,
    memory_format: Optional[torch.memory_format] = None,
) -> torch.memory_format:
    # TODO: _to_copy tensor to stride permutation
    if memory_format is torch.preserve_format or memory_format is None:
        return utils.suggest_memory_format(tensor)
    else:
        return memory_format
