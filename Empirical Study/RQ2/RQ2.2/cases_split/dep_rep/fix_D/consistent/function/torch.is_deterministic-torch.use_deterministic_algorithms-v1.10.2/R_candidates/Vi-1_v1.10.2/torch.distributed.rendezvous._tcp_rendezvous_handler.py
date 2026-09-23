def _tcp_rendezvous_handler(
    url: str, timeout: timedelta = default_pg_timeout, **kwargs
):
    def _error(msg):
        return _rendezvous_error("tcp:// rendezvous: " + msg)

    result = urlparse(url)
    if not result.port:
        raise _error("port number missing")
    query: Dict[str, Union[int, str]]
    # mypy doesn't allow dict() to accept List of values (#257)
    query = dict(pair.split("=") for pair in filter(None, result.query.split("&")))  # type: ignore[misc, arg-type]
    if "rank" not in query:
        raise _error("rank parameter missing")
    if "world_size" not in query:
        raise _error("world size parameter missing")

    rank = int(query["rank"])
    world_size = int(query["world_size"])
    assert result.hostname is not None

    store = _create_c10d_store(result.hostname, result.port, rank, world_size, timeout)

    yield (store, rank, world_size)

    # If this configuration is invalidated, there is nothing we can do about it
    raise RuntimeError("Unable to perform re-rendezvous using tcp:// method")
