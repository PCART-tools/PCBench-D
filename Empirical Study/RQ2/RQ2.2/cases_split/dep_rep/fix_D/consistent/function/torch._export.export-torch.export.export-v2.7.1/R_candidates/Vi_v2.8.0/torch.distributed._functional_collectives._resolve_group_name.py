def _resolve_group_name(group: RANK_TYPES, tag: str = "") -> str:
    """
    Given group in RANK_TYPES, return the group name.
    """
    # `tag` will be deprecated. See details in:
    # https://github.com/pytorch/pytorch/issues/93173#issuecomment-1907095208
    if isinstance(group, dist.ProcessGroup):
        return group.group_name
    elif isinstance(group, str):
        return group
    elif isinstance(group, DeviceMesh):
        assert group.ndim == 1, (
            "Only 1D mesh is supported, pass in (DeviceMesh, int) together if mesh > 1D"
        )
        return group._dim_group_names[0]
    elif isinstance(group, tuple):
        if (
            len(group) == 2
            and isinstance(group[0], DeviceMesh)
            and isinstance(group[1], int)
        ):
            dmesh = group[0]
            dim = group[1]
            return dmesh._dim_group_names[dim]
        else:
            raise ValueError("Invalid tuple for group must be (DeviceMesh, int)")
    elif isinstance(group, list):
        if not is_torchdynamo_compiling():
            warnings.warn(
                "The combination of ranks + tag as process group "
                "identifier has been deprecated. Please switch to "
                "using ProcessGroup, DeviceMesh, or group name instead.",
                FutureWarning,
                stacklevel=3,
            )
        return c10d._resolve_group_name_by_ranks_and_tag(cast(list[int], group), tag)
    else:
        raise ValueError(f"Unsupported group type: {type(group)}, {group}")
