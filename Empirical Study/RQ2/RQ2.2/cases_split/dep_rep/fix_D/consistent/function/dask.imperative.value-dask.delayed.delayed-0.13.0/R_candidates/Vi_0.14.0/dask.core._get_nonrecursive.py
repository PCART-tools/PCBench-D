def _get_nonrecursive(d, x, maxdepth=1000):
    # Non-recursive. DAG property is checked upon reaching maxdepth.
    _list = lambda *args: list(args)

    # We construct a nested hierarchy of tuples to mimic the execution stack
    # of frames that Python would maintain for a recursive implementation.
    # A frame is associated with a single task from a Dask.
    # A frame tuple has three elements:
    #    1) The function for the task.
    #    2) The arguments for the task (typically keys in the Dask).
    #       Arguments are stored in reverse order, and elements are popped
    #       as they are evaluated.
    #    3) The calculated results of the arguments from (2).
    stack = [(lambda x: x, [x], [])]
    while True:
        func, args, results = stack[-1]
        if not args:
            val = func(*results)
            if len(stack) == 1:
                return val
            stack.pop()
            stack[-1][2].append(val)
            continue
        elif maxdepth and len(stack) > maxdepth:
            cycle = getcycle(d, x)
            if cycle:
                cycle = '->'.join(cycle)
                raise RuntimeError('Cycle detected in Dask: %s' % cycle)
            maxdepth = None

        key = args.pop()
        if isinstance(key, list):
            stack.append((_list, list(key[::-1]), []))
            continue
        elif ishashable(key) and key in d:
            args.append(d[key])
            continue
        elif istask(key):
            stack.append((key[0], list(key[:0:-1]), []))
        else:
            results.append(key)
