def _get_group_size(group):
    """
    Helper that gets a given group's world size.
    """
    if group is GroupMember.WORLD or group is None:
        default_pg = _get_default_group()
        return default_pg.size()
    return group.size()
