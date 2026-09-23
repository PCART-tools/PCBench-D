def _check_full_rank(store, world_size):
    idx = store.add(_MEMBER_CHECKIN, 1)
    if idx == world_size:
        store.set(_LAST_MEMBER_CHECKIN, "<val_ignored>")

    try:
        store.get(_LAST_MEMBER_CHECKIN)
    except RuntimeError as e:
        if str(e) == _SOCKET_TIMEOUT:
            raise TimeoutError(
                f"timed out waiting for all {world_size} members to join"
            ) from e
        else:
            raise
