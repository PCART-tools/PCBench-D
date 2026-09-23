def rendezvous(url: str, rank: int = -1, world_size: int = -1, **kwargs):
    if not isinstance(url, (str, bytes)):
        raise RuntimeError(f"`url` must be a string. {type(url)}: {url}")

    if not isinstance(rank, numbers.Integral):
        raise RuntimeError(f"`rank` must be an integer. {rank}")

    if not isinstance(world_size, numbers.Integral):
        raise RuntimeError(f"`world_size` must be an integer. {world_size}")

    return _rendezvous_helper(url, rank, world_size, **kwargs)
