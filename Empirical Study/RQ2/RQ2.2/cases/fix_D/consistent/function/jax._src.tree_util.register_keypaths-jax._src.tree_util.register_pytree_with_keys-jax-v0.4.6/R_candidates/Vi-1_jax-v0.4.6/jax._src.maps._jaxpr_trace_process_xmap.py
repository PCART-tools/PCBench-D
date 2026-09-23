def _jaxpr_trace_process_xmap(self, primitive, f: lu.WrappedFun, tracers, params):
  assert primitive is xmap_p
  assert params['spmd_out_axes_thunk'] is params['spmd_in_axes'] is None
  in_axes = params['in_axes']
  donated_invars = params['donated_invars']
  global_axis_sizes = params['global_axis_sizes']
  out_axes_thunk = params['out_axes_thunk']

  # Adjust input tracers' pvals for mapped axes, and unpack.
  in_pvals = [t.pval if t.pval.is_known() else
              pe.PartialVal.unknown(
                  _delete_aval_axes(t.pval.get_aval(), axes, global_axis_sizes))
              for t, axes in zip(tracers, in_axes)]
  in_knowns, in_avals, in_consts = pe.partition_pvals(in_pvals)

  # Wrap f to perform partial evaluation, and plumb out aux data.
  f = pe.trace_to_subjaxpr_nounits(f, self.main, False)
  f, aux = pe.partial_eval_wrapper_nounits(f, tuple(in_knowns), tuple(in_avals))
  # Also grab the local named shapes of the output (known and res).
  f, out_named_shapes = out_local_named_shapes(f, frozenset(global_axis_sizes))

  # Adjust params for knowns (donated_invars, in_axes, out_axes_thunk).
  out_axes = None  # cache this to avoid calling out_axes_thunk() more than once

  @as_hashable_function(closure=out_axes_thunk)
  def new_out_axes_thunk():
    nonlocal out_axes
    out_axes = out_axes_thunk()
    out_knowns, _, _, _ = aux()
    _, out_axes_known = partition_list(out_knowns, out_axes)
    return (*out_axes_known, *res_axes())
  def res_axes():
    _, _, jaxpr_unknown, _ = aux()
    num_res = len(jaxpr_unknown.constvars)
    res_named_shapes = out_named_shapes()[-num_res:] if num_res else []
    sorted_named_shapes = [sorted(ns, key=str) for ns in res_named_shapes]
    return [AxisNamePos(zip(named_shape, range(len(named_shape))),
                        user_repr=f'<internal: {named_shape}>')
            for named_shape in sorted_named_shapes]
  known_params = dict(
      params, in_axes=tuple(a for a, k in zip(in_axes, in_knowns) if k),
      donated_invars=tuple(d for d, k in zip(donated_invars, in_knowns) if k),
      out_axes_thunk=new_out_axes_thunk)

  # Run the known part.
  out = primitive.bind(f, *in_consts, **known_params)
  out_knowns, out_avals, jaxpr_unknown, env = aux()
  known_outvals, res = split_list(out, [len(out)-len(jaxpr_unknown.constvars)])
  with core.extend_axis_env_nd(global_axis_sizes.items()):
    jaxpr_unknown = pe.convert_constvars_jaxpr(jaxpr_unknown)

  # Set up new params.
  if out_axes is None:
    out_axes = out_axes_thunk()  # new_out_axes_thunk may have set during bind
  out_axes_unknown = [a for a, k in zip(out_axes, out_knowns) if not k]
  unknown_params = dict(
      params, call_jaxpr=jaxpr_unknown, out_axes=tuple(out_axes_unknown),
      spmd_out_axes=None,
      donated_invars=(*(False for _ in res),
                      *(d for d, k in zip(donated_invars, in_knowns) if not k)),
      in_axes=(*res_axes(), *(None for _ in env),
               *(a for a, k in zip(in_axes, in_knowns) if not k)))
  del unknown_params['out_axes_thunk']
  del unknown_params['spmd_out_axes_thunk']
  # Create input tracers for unknown part.
  res_tracers = map(self.new_instantiated_const, res)
  env_tracers = map(self.full_raise, env)
  unknown_arg_tracers = [t for t in tracers if not t.pval.is_known()]
  # Create output tracers for unknown part, adjusting avals.
  axis_resource_count = _get_axis_resource_count(
      params['axis_resources'], params['resource_env'],
      params['in_positional_semantics'])
  local_axis_sizes = {
      ax: axis_resource_count[ax].to_local(
          params['out_positional_semantics'], global_size)
      for ax, global_size in global_axis_sizes.items()}
  out_pvals = [pe.PartialVal.unknown(_insert_aval_axes(a, ax, local_axis_sizes))
               for a, ax in zip(out_avals, out_axes_unknown)]
  unknown_tracers_out = [pe.JaxprTracer(self, pval, None) for pval in out_pvals]
  # Build eqn to be staged out and attach it to unknown output tracers.
  eqn = pe.new_eqn_recipe((*res_tracers, *env_tracers, *unknown_arg_tracers),
                          unknown_tracers_out, primitive, unknown_params,
                          jaxpr_unknown.effects, source_info_util.current())
  for t in unknown_tracers_out: t.recipe = eqn
  return merge_lists(out_knowns, unknown_tracers_out, known_outvals)
