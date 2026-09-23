def destroy_process_group(group=None):
    """
    Destroy a given process group, and deinitialize the distributed package

    Args:
        group (ProcessGroup, optional): The process group to be destroyed, if
                                        group.WORLD is given, all process
                                        groups including the default one will
                                        be destroyed.
    """
    global _pg_map
    global _pg_names
    global _pg_group_ranks
    global _default_pg_init_method
    global _group_count

    if group == GroupMember.NON_GROUP_MEMBER:
        return

    if group is None:
        pg = GroupMember.WORLD
    else:
        pg = group

    assert pg is not None
    if _pg_map.get(pg, None) is None:
        raise RuntimeError("Invalid process group specified")

    if group is None or group == GroupMember.WORLD:
        _update_default_pg(None)
        _default_pg_init_method = None
        _pg_map.clear()
        _pg_names.clear()
        _pg_group_ranks.clear()

        # when process group doesn't have an explicit name (only WORLD (default)
        # process group can have an explicit name), we use global _group_counter
        # to generate the name. We need to reset the counter on destruction to
        # allow consistent value to be generated when we re-create process
        # groups after some trainers recover from failure
        #
        # We only reset this when WORLD is being destroyed because if this
        # process group is in good state, we aren't dealing with failures.
        _group_count = 0
    else:
        del _pg_map[pg]
        del _pg_names[pg]
        del _pg_group_ranks[pg]
