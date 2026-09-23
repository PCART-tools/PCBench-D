def normalize_sizes(sizes: Union[Shape, tuple[Shape]]) -> Shape:
    if isinstance(sizes[0], int):
        return cast(Shape, sizes)
    elif len(sizes) == 1:
        return sizes[0]
    else:
        raise RuntimeError("Size must be int... or tuple")
