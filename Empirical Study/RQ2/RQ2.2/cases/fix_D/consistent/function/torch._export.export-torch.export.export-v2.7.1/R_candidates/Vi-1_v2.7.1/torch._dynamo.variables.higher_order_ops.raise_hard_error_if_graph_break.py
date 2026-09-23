def raise_hard_error_if_graph_break(reason):
    def deco(fn):
        @functools.wraps(fn)
        def graph_break_as_hard_error(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Unsupported as e:
                msg = " Scroll up to find out what causes the graph break."
                raise UncapturedHigherOrderOpError(reason + msg) from e

        return graph_break_as_hard_error

    return deco
