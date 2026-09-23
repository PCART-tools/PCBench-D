def hold_keys(dsk, dependencies):
    """ Find keys to avoid fusion

    We don't want to fuse data present in the graph because it is easier to
    serialize as a raw value.

    We don't want to fuse chains after getitem/GETTERS because we want to
    move around only small pieces of data, rather than the underlying arrays.
    """
    dependents = reverse_dict(dependencies)
    data = {k for k, v in dsk.items() if type(v) not in (tuple, str)}

    hold_keys = list(data)
    for dat in data:
        deps = dependents[dat]
        for dep in deps:
            task = dsk[dep]
            # If the task is a get* function, we walk up the chain, and stop
            # when there's either more than one dependent, or the dependent is
            # no longer a get* function or an alias. We then add the final
            # key to the list of keys not to fuse.
            if type(task) is tuple and task and task[0] in GETTERS:
                try:
                    while len(dependents[dep]) == 1:
                        new_dep = next(iter(dependents[dep]))
                        new_task = dsk[new_dep]
                        # If the task is a get* or an alias, continue up the
                        # linear chain
                        if new_task[0] in GETTERS or new_task in dsk:
                            dep = new_dep
                        else:
                            break
                except (IndexError, TypeError):
                    pass
                hold_keys.append(dep)
    return hold_keys
