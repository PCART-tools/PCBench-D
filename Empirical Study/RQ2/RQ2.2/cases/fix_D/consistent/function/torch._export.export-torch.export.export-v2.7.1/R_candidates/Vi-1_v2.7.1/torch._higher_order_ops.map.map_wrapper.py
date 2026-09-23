def map_wrapper(f, xs, *args):
    flat_xs, xs_spec = pytree.tree_flatten(xs)
    if not all(isinstance(t, torch.Tensor) for t in flat_xs):
        raise RuntimeError(f"Mapped xs can only consist of tensors. Got xs {flat_xs}.")

    num_mapped_args = len(flat_xs)
    shapes = [xs.shape for xs in flat_xs]
    leading_dim_size = shapes[0][0]
    if leading_dim_size == 0:
        raise RuntimeError("Leading dimensions of mapped xs cannot be 0.")

    if any(cur_shape[0] != leading_dim_size for cur_shape in shapes):
        raise RuntimeError(
            f"Leading dimensions of mapped xs must be consistent. Got shapes {shapes}."
        )

    out_spec = None

    def flat_fn(*flat_args):
        xs = pytree.tree_unflatten(list(flat_args[:num_mapped_args]), xs_spec)
        unflattened_out = f(xs, *flat_args[num_mapped_args:])
        flat_out, tmp_out_spec = pytree.tree_flatten(unflattened_out)

        nonlocal out_spec
        out_spec = tmp_out_spec
        return flat_out

    return pytree.tree_unflatten(
        map_impl(flat_fn, flat_xs, args), out_spec  # type: ignore[arg-type]
    )
