def enable_symm_mem_for_group(group_name: str) -> None:
    """
    Enables symmetric memory for a process group.

    Args:
        group_name (str): the name of the process group.
    """
    if group_name in _group_name_to_store:
        return

    group = c10d._resolve_process_group(group_name)
    global_ranks = sorted(c10d._world.pg_group_ranks[group].keys())
    # Different subgroups with the same name should use different stores
    global_ranks_str = "_".join(map(str, global_ranks))
    store = c10d.PrefixStore(
        f"symmetric_memory-{global_ranks_str}",
        c10d._get_process_group_store(group),
    )
    # Use one store-based broadcast to bootstrap a file store from the process
    # and simultaneously verify that all ranks are on the same host.
    hostname = socket.gethostname()
    if group.rank() == 0:
        uid = str(uuid.uuid4())
        msg = f"{hostname}/{uid}"
        store.set("init", msg)
    else:
        msg = store.get("init").decode("utf-8")
        tokens = msg.split("/")
        assert len(tokens) == 2, tokens
        rank_0_hostname, uid = tokens
        if hostname != rank_0_hostname:
            raise RuntimeError(
                "init_symmetric_memory_for_process_group() failed for "
                f'group "{group_name}". Rank 0 and rank {group.rank()} '
                f"are on different hosts ({rank_0_hostname} and {hostname})"
            )
    store = torch._C._distributed_c10d.FileStore(f"/tmp/{uid}", group.size())
    # TODO: check device connectiivity
    _group_name_to_store[group_name] = store
    _SymmetricMemory.set_group_info(
        group_name,
        group.rank(),
        group.size(),
        store,
    )
