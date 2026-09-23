def all_to_all_single_autograd(
    self: torch.Tensor,
    output_split_sizes: Optional[list[int]],
    input_split_sizes: Optional[list[int]],
    group: RANK_TYPES,
    tag: str = "",
) -> torch.Tensor:
    """
    Same as all_to_all_single but supports autograd.
    """
    if output_split_sizes is not None:
        assert all(
            isinstance(size, (int, torch.SymInt)) for size in output_split_sizes
        ), output_split_sizes
    if input_split_sizes is not None:
        assert all(
            isinstance(size, (int, torch.SymInt)) for size in input_split_sizes
        ), input_split_sizes

    group_name = _resolve_group_name(group, tag)
    group_size = c10d._get_group_size_by_name(group_name)
    if output_split_sizes is None or input_split_sizes is None:
        assert output_split_sizes is None and input_split_sizes is None, (
            "output_split_sizes and input_split_sizes must either be "
            "specified together or both set to None"
        )
        output_split_sizes = [self.shape[0] // group_size] * group_size
        input_split_sizes = output_split_sizes
    tensor = torch.ops._c10d_functional_autograd.all_to_all_single(  # type: ignore[attr-defined]
        self,
        output_split_sizes,
        input_split_sizes,
        group_name,
    )
    return _FromTorchTensor.apply(tensor)
