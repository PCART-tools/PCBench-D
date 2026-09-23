def pallas_call(
    f: Callable[..., None],
    out_shape: Any,
    *,
    grid_spec: GridSpec | None = None,
    debug: bool = False,
    grid: Grid | None = None,
    in_specs: Sequence[BlockSpec | NoBlockSpec] | NoBlockSpec = no_block_spec,
    out_specs: BlockSpec | NoBlockSpec
    | Sequence[BlockSpec | NoBlockSpec] = no_block_spec,
    input_output_aliases: dict[int, int] = {},
    interpret: bool = False,
    name: str | None = None,
    **compiler_params: Any,
):
  name = _extract_function_name(f, name)
  if grid is not None and grid_spec is not None:
    raise ValueError("Cannot specify both grid and grid_spec at the same time.")
  if grid_spec is None:
    grid_spec = GridSpec(grid, in_specs, out_specs)
  grid_spec, dynamic_grid_bounds = grid_spec.unzip_dynamic_grid_bounds()
  if isinstance(out_shape, list):
    out_shape = tuple(out_shape)
  flat_out_shapes, out_tree = tree_util.tree_flatten(out_shape)
  flat_out_shapes = [jax.ShapeDtypeStruct(x.shape, x.dtype)
                     for x in flat_out_shapes]
  @jax.jit
  def wrapped(*args):
    flat_args, in_tree = tree_util.tree_flatten(args)
    flat_in_avals = tuple(jax_core.raise_to_shaped(jax_core.get_aval(a))
                          for a in flat_args)
    flat_out_avals = tuple(jax_core.ShapedArray(v.shape, v.dtype)
                           for v in flat_out_shapes)
    grid_mapping, jaxpr, consts, _ = _trace_to_jaxpr(
        f, grid_spec, flat_in_avals, flat_out_avals, in_tree,
        out_tree)
    which_linear = (False,) * len(flat_args)
    out_flat = pallas_call_p.bind(
        *dynamic_grid_bounds, *consts, *flat_args,
        jaxpr=jaxpr, name=name, which_linear=which_linear,
        in_shapes=tuple(jax.ShapeDtypeStruct(a.shape, a.dtype)
                        for a in flat_args),
        out_shapes=tuple(flat_out_shapes), debug=debug,
        interpret=interpret,
        grid_mapping=grid_mapping,
        input_output_aliases=tuple(input_output_aliases.items()),
        **compiler_params)
    out = tree_util.tree_unflatten(out_tree, out_flat)
    return out
  return wrapped
