def _uninstall_threaded_pg():
    dist.distributed_c10d._world = _old_pg_world
