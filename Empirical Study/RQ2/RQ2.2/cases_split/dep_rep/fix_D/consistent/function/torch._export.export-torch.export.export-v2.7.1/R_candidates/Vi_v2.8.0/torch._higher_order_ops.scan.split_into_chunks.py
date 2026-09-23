def split_into_chunks(iterable: Sequence[Any], chunk_sizes: list[int]) -> list[Any]:
    it = iter(iterable)
    assert sum(chunk_sizes) == len(
        iterable
    ), "the sum of all chunks needs to match the length of the iterable."
    return [list(itertools.islice(it, size)) for size in chunk_sizes]
