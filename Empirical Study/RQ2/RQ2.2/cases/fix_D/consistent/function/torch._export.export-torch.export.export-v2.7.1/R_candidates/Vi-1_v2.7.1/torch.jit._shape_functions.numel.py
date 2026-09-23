def numel(sizes: list[int]):
    numel = 1
    for elem in sizes:
        numel *= elem
    return numel
