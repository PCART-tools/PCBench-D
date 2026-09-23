def mask(fun: Callable, in_shapes, out_shape=None) -> Callable:
  warn("`jax.mask` is deprecated and will be removed soon. ",
       DeprecationWarning)
  _check_callable(fun)
  unique_ids = masking.UniqueIds()

  in_specs, in_shapes_tree = tree_flatten(in_shapes)
  in_specs = map(masking.parse_spec, in_specs)
  in_specs = map(partial(masking.remap_ids, unique_ids), in_specs)

  if out_shape is not None:
    out_specs, out_spec_tree = tree_flatten(out_shape)
    out_specs = map(masking.parse_spec, out_specs)
    out_specs = map(partial(masking.remap_ids, unique_ids), out_specs)

  def wrapped_fun(args, logical_env):
    args_flat, in_tree = tree_flatten(args)
    if in_tree != in_shapes_tree:
      raise TypeError(f"Tree mismatch: Input {in_tree} and shape spec {in_shapes_tree}.")
    logical_env = {unique_ids[name] : val for name, val in logical_env.items()}
    in_shapes = map(masking.finalize_spec, in_specs, map(np.shape, args_flat))
    padded_env = masking.bind_shapes(in_shapes, [x.shape for x in args_flat])
    f = lu.wrap_init(fun)
    flat_fun, out_tree_thunk = flatten_fun_nokwargs(f, in_tree)
    outs, out_shapes = masking.mask_fun(
      flat_fun, logical_env, padded_env, args_flat, in_shapes)
    out_tree = out_tree_thunk()

    if out_shape is None:
      def logical_shape(poly_shape, padded_val):
        shape = masking.eval_poly_shape(poly_shape, logical_env)
        return ShapeDtypeStruct(shape, core.get_aval(padded_val).dtype)
      out_logicals = map(logical_shape, out_shapes, outs)
      return tree_unflatten(out_tree, outs), tree_unflatten(out_tree, out_logicals)
    else:
      masking.check_shapes(out_specs, out_spec_tree, list(out_shapes), out_tree)
      def padded_spec(shape_spec):
        return tuple(dim if dim is masking._monomorphic_dim else
                     masking.eval_poly(dim, padded_env) for dim in shape_spec)
      masking.check_shapes(map(padded_spec, out_specs), out_spec_tree,
                           map(np.shape, outs), out_tree, "Padded output")
      return tree_unflatten(out_tree, outs)
  return wrapped_fun
