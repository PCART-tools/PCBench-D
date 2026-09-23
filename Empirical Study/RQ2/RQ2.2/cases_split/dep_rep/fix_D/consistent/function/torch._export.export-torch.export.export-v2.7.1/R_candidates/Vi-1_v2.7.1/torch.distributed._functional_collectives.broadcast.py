def broadcast(self: torch.Tensor, src: int, group: RANK_TYPES, tag: str = ""):
    """
    Broadcasts the tensor to all processes in the given process group.

    Args:
        src (int): Source rank
        group (ProcessGroup or List[int]): The process group to work on.
        tag (str, optional): A unique identifier for the collective. Default: empty string
    """
    group_name = _resolve_group_name(group, tag)
    tensor = torch.ops._c10d_functional.broadcast(self, src, group_name)
    return _maybe_wrap_tensor(tensor)
