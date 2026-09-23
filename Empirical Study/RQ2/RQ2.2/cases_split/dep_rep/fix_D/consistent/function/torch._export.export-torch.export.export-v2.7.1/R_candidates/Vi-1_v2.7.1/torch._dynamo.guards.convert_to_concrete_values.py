def convert_to_concrete_values(size_or_stride):
    converted: list[Optional[int]] = []
    for dim in size_or_stride:
        if not is_symbolic(dim):
            converted.append(dim)
        else:
            assert isinstance(dim, torch.SymInt)
            converted.append(dim.node.maybe_as_int())
    return converted
