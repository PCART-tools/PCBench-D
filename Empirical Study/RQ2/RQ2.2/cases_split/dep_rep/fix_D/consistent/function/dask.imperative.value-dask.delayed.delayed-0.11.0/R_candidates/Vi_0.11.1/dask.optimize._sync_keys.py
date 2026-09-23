def _sync_keys(dsk1, dsk2, dsk2_topo):
    dep_dict1 = dependency_dict(dsk1)
    subs = {}

    for key2 in toposort(dsk2):
        deps = tuple(get_dependencies(dsk2, key2, True))
        # List of keys in dsk1 that have terms that *may* match key2
        possible_matches = _possible_matches(dep_dict1, deps, subs)
        if possible_matches:
            val2 = dsk2[key2]
            for key1 in possible_matches:
                val1 = dsk1[key1]
                if equivalent(val1, val2, subs):
                    subs[key2] = key1
                    break
    return subs
