def gen_transitive_closure(
    dep_graph: DepGraph,
    root_ops: List[str],
    train: bool = False,
) -> List[str]:
    result = set(root_ops)
    queue = root_ops[:]

    # The dependency graph might contain a special entry with key = `__BASE__`
    # and value = (set of `base` ops to always include in custom build).
    queue.append('__BASE__')

    # The dependency graph might contain a special entry with key = `__ROOT__`
    # and value = (set of ops reachable from C++ functions). Insert the special
    # `__ROOT__` key to include ops which can be called from C++ code directly,
    # in addition to ops that are called from TorchScript model.
    # '__ROOT__' is only needed for full-jit. Keep it only for training.
    # TODO: when FL is migrated from full-jit to lite trainer, remove '__ROOT__'
    if train:
        queue.append('__ROOT__')

    while queue:
        cur = queue.pop()
        for dep in dep_graph.get(cur, []):
            if dep not in result:
                result.add(dep)
                queue.append(dep)

    return sorted(result)
