def pallas_call(
    f: Callable[..., None], out_shape: Any, *,
    grid_spec: GridSpec | None = None,
    debug: bool = False,
    grid: Grid | None = None,
    in_specs: Sequence[BlockSpec | None] | None = None,
    out_specs: BlockSpec | Sequence[BlockSpec | None] | None = None,
    input_output_aliases: Dict[int, int] = {},
    interpret: bool = False,
    name: str | None = None,
    **compiler_params: Any):
  if grid_spec is None:
    grid_spec = GridSpec(grid, in_specs, out_specs)
  name = _extract_function_name(f, name)
  singleton = False
  if not isinstance(out_shape, (tuple, list)):
    out_shape = (out_shape,)
    singleton = True
  if not isinstance(out_shape, tuple):
    out_shape = tuple(out_shape)
  flat_out_shapes, out_tree = tree_util.tree_flatten(out_shape)
  flat_out_shapes = [jax.ShapeDtypeStruct(x.shape, x.dtype)
                     for x in flat_out_shapes]
  @jax.jit
  def wrapped(*args):
    flat_args, in_tree = tree_util.tree_flatten(args)
    flat_avals = [jax_core.raise_to_shaped(jax_core.get_aval(a))
                  for a in flat_args]
    avals, grid_mapping = grid_spec.get_grid_mapping(flat_avals, in_tree,
                                                     flat_out_shapes, out_tree)
    jaxpr_flat_avals, jaxpr_in_tree = tree_util.tree_flatten(avals)
    jaxpr, consts, _ = _initial_style_open_jaxpr(f, jaxpr_in_tree,
                                                 tuple(jaxpr_flat_avals),
                                                 primitive_name="pallas_call")
    which_linear = (False,) * len(flat_args)
    out_flat = pallas_call_p.bind(
        *consts, *flat_args, jaxpr=jaxpr, name=name, which_linear=which_linear,
        in_shapes=tuple(jax.ShapeDtypeStruct(a.shape, a.dtype)
                        for a in flat_args),
        out_shapes=tuple(flat_out_shapes), debug=debug,
        interpret=interpret,
        grid_mapping=grid_mapping,
        input_output_aliases=tuple(input_output_aliases.items()),
        **compiler_params)
    out = tree_util.tree_unflatten(out_tree, out_flat)
    if singleton:
      return out[0]
    return out
  return wrapped
