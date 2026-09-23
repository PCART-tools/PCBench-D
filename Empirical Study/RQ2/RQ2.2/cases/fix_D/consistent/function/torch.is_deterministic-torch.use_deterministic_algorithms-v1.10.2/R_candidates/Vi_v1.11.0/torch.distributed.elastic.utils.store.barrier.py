def barrier(
    store, rank: int, world_size: int, key_prefix: str, barrier_timeout: float = 300
) -> None:
    """
    A global lock between agents.

    Note: Since the data is not removed from the store, the barrier can be used
        once per unique ``key_prefix``.
    """
    data = f"{rank}".encode(encoding="UTF-8")
    synchronize(store, data, rank, world_size, key_prefix, barrier_timeout)
