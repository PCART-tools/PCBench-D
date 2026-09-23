def _get_single_group_name(rx):
    try:
        return list(rx.groupindex.keys()).pop()
    except IndexError:
        return None
