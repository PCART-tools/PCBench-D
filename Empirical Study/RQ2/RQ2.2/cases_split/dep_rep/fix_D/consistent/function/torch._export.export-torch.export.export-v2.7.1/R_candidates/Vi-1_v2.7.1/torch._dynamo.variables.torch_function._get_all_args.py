def _get_all_args(args, kwargs):
    return _flatten_vts(pytree.arg_tree_leaves(*args, **kwargs))
