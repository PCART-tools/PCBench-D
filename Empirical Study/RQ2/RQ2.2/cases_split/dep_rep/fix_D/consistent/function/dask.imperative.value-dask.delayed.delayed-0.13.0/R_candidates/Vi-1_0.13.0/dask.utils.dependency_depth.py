def dependency_depth(dsk):
    import toolz

    deps, _ = get_deps(dsk)

    @toolz.memoize
    def max_depth_by_deps(key):
        if not deps[key]:
            return 1

        d = 1 + max(max_depth_by_deps(dep_key) for dep_key in deps[key])
        return d

    return max(max_depth_by_deps(dep_key) for dep_key in deps.keys())
