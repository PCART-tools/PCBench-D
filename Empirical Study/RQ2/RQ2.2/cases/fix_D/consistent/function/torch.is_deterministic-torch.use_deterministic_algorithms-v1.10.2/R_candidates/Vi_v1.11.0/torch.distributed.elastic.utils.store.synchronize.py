def synchronize(
    store,
    data: bytes,
    rank: int,
    world_size: int,
    key_prefix: str,
    barrier_timeout: float = 300,
) -> List[bytes]:
    """
    Synchronizes ``world_size`` agents between each other using the underlying c10d store.
    The ``data`` will be available on each of the agents.

    Note: The data on the path is not deleted, as a result there can be stale data if
        you use the same key_prefix twice.
    """
    store.set_timeout(timedelta(seconds=barrier_timeout))
    store.set(f"{key_prefix}{rank}", data)
    agent_data = get_all(store, key_prefix, world_size)
    return agent_data
