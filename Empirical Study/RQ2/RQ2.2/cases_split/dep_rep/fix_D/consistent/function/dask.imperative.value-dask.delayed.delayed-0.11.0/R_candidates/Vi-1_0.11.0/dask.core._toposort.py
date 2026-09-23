def _toposort(dsk, keys=None, returncycle=False, dependencies=None):
    # Stack-based depth-first search traversal.  This is based on Tarjan's
    # method for topological sorting (see wikipedia for pseudocode)
    if keys is None:
        keys = dsk
    elif not isinstance(keys, list):
        keys = [keys]
    if not returncycle:
        ordered = []

    # Nodes whose descendents have been completely explored.
    # These nodes are guaranteed to not be part of a cycle.
    completed = set()

    # All nodes that have been visited in the current traversal.  Because
    # we are doing depth-first search, going "deeper" should never result
    # in visiting a node that has already been seen.  The `seen` and
    # `completed` sets are mutually exclusive; it is okay to visit a node
    # that has already been added to `completed`.
    seen = set()

    if dependencies is None:
        dependencies = dict((k, get_dependencies(dsk, k)) for k in dsk)

    for key in keys:
        if key in completed:
            continue
        nodes = [key]
        while nodes:
            # Keep current node on the stack until all descendants are visited
            cur = nodes[-1]
            if cur in completed:
                # Already fully traversed descendants of cur
                nodes.pop()
                continue
            seen.add(cur)

            # Add direct descendants of cur to nodes stack
            next_nodes = []
            for nxt in dependencies[cur]:
                if nxt not in completed:
                    if nxt in seen:
                        # Cycle detected!
                        cycle = [nxt]
                        while nodes[-1] != nxt:
                            cycle.append(nodes.pop())
                        cycle.append(nodes.pop())
                        cycle.reverse()
                        if returncycle:
                            return cycle
                        else:
                            cycle = '->'.join(cycle)
                            raise RuntimeError('Cycle detected in Dask: %s' % cycle)
                    next_nodes.append(nxt)

            if next_nodes:
                nodes.extend(next_nodes)
            else:
                # cur has no more descendants to explore, so we're done with it
                if not returncycle:
                    ordered.append(cur)
                completed.add(cur)
                seen.remove(cur)
                nodes.pop()
    if returncycle:
        return []
    return ordered
