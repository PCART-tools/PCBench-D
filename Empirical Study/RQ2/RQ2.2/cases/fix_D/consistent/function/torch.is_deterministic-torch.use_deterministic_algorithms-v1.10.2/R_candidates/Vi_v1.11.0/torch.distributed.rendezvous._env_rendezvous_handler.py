def _env_rendezvous_handler(
    url: str, timeout: timedelta = default_pg_timeout, **kwargs
):
    def _error(msg):
        return _rendezvous_error("env:// rendezvous: " + msg)

    def _env_error(var):
        return _error("environment variable %s expected, but not set" % var)

    def _get_env_or_raise(env_var: str) -> str:
        env_val = os.environ.get(env_var, None)
        if not env_val:
            raise _env_error(env_var)
        else:
            return env_val

    result = urlparse(url)
    query: Dict[str, Union[int, str]]
    # mypy doesn't allow dict() to accept List of values (#257)
    query = dict(pair.split("=") for pair in filter(None, result.query.split("&")))  # type: ignore[misc, arg-type]

    rank: Optional[Union[str, int]]
    world_size: Optional[Union[str, int]]
    master_port: Optional[Union[str, int]]

    if "rank" in query:
        rank = int(query["rank"])
    else:
        rank = int(_get_env_or_raise("RANK"))

    if "world_size" in query:
        world_size = int(query["world_size"])
    else:
        world_size = int(_get_env_or_raise("WORLD_SIZE"))

    master_addr = _get_env_or_raise("MASTER_ADDR")
    master_port = int(_get_env_or_raise("MASTER_PORT"))

    store = _create_c10d_store(master_addr, master_port, rank, world_size, timeout)

    yield (store, rank, world_size)

    # If this configuration is invalidated, there is nothing we can do about it
    raise RuntimeError("Unable to perform re-rendezvous using env:// method")
