def wrap_combine_fn_flat(*args, combine_fn, spec, num_leaves):
    assert (
        len(args) == 2 * num_leaves
    ), f"Combin_fn received wrong number of arguments, expected {2 * num_leaves}, but got {len(args)}"
    lhs = pytree.tree_unflatten(args[:num_leaves], spec)
    rhs = pytree.tree_unflatten(args[num_leaves:], spec)
    return combine_fn(lhs, rhs)
