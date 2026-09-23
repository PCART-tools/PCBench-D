def single_ellipsis_index(names, fn_name):
    ellipsis_indices = [i for i, name in enumerate(names) if is_ellipsis(name)]
    if len(ellipsis_indices) >= 2:
        raise RuntimeError('{}: More than one Ellipsis (\'...\') found in names ('
                           '{}). This function supports up to one Ellipsis.'
                           .format(fn_name, names))
    if len(ellipsis_indices) == 1:
        return ellipsis_indices[0]
    return None
