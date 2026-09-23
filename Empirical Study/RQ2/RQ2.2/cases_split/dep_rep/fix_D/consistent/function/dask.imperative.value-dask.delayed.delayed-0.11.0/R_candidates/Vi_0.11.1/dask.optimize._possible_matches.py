def _possible_matches(dep_dict, deps, subs):
    deps2 = []
    for d in deps:
        v = subs.get(d, None)
        if v is not None:
            deps2.append(v)
        else:
            return []
    deps2 = tuple(deps2)
    return dep_dict.get(deps2, [])
