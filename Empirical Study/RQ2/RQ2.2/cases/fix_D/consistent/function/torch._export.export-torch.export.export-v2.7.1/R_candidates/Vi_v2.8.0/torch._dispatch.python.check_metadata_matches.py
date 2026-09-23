def check_metadata_matches(n, r, desc):
    assert callable(desc)
    n_vals, _n_spec = pytree.tree_flatten(n)
    r_vals, _r_spec = pytree.tree_flatten(r)
    # TODO: test the specs match; empirically  sometimes we have a tuple
    # on one side and a list on the other
    assert len(n_vals) == len(r_vals), f"{len(n_vals)} != {len(r_vals)}"
    for i, nv, rv in zip(range(len(n_vals)), n_vals, r_vals):
        if not isinstance(rv, torch.Tensor):
            continue
        check_tensor_metadata_matches(nv, rv, lambda: f"{desc()} output {i}")
