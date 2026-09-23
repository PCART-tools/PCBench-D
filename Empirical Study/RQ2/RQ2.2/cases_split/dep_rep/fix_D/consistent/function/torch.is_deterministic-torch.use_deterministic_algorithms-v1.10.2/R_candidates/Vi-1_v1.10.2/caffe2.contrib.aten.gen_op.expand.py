def expand(o):
    num_defaults = sum(1 if 'default' in arg else 0 for arg in o['arguments'])
    results = [o]
    for i in range(0, num_defaults):
        # last num_default values should be default
        assert('default' in o['arguments'][-(i + 1)])
        v = deepcopy(o)
        v['arguments'] = v['arguments'][:-(i + 1)]
        results.append(v)
    return results
