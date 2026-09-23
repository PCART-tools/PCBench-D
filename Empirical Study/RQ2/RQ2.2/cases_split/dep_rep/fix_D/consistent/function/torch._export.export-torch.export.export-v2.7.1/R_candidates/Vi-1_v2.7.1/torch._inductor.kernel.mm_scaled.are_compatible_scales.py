def are_compatible_scales(size_a: Sequence[int], size_b: Sequence[int]) -> bool:
    # Same sized scales are compatable
    if len(size_a) == len(size_b):
        return True

    # Both need to be scalars or len(1) tensors
    if len(size_a) <= 1 and len(size_b) <= 1:
        return True

    return False
