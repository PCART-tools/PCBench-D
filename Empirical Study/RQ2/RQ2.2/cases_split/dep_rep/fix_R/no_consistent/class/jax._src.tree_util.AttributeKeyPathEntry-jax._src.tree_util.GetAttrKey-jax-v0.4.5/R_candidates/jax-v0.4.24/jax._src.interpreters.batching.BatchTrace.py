class BatchTrace(Trace):

  def __init__(self, *args, axis_name, spmd_axis_name = None):
    super().__init__(*args)
    self.axis_name = axis_name
    self.spmd_axis_name = spmd_axis_name

  def pure(self, val):
    return BatchTracer(self, val, not_mapped, source_info_util.current())

  def lift(self, val):
    return BatchTracer(self, val, not_mapped, source_info_util.current())

  def sublift(self, val):
    return BatchTracer(self, val.val, val.batch_dim, source_info_util.current())

  def get_primitive_batcher(self, primitive, frame):
    if primitive in primitive_batchers:
      return primitive_batchers[primitive]
    elif self.spmd_axis_name is not None and primitive in spmd_axis_primitive_batchers:
      return partial(spmd_axis_primitive_batchers[primitive],
                     self.spmd_axis_name, frame.size, frame.name,
                     frame.main_trace.trace_type)
    elif primitive in axis_primitive_batchers:
      return self.get_axis_primitive_batcher(primitive, frame)
    msg = "Batching rule for '{}' not implemented"
    raise NotImplementedError(msg.format(primitive))

  def get_axis_primitive_batcher(self, primitive, frame):
    return partial(axis_primitive_batchers[primitive],
        frame.size, frame.name, frame.main_trace.trace_type)

  def get_frame(self, vals, dims) -> core.AxisEnvFrame:
    if any(d is not not_mapped for d in dims):
      sizes = (x.shape[d] if type(d) is int else d.size
               for x, d in zip(vals, dims) if d is not not_mapped)
      axis_size, = core.dedup_referents(sizes)
    else:
      axis_size = None  # can't be inferred from data
    if self.axis_name is core.no_axis_name:
      assert axis_size is not None  # must be inferable from data
      return core.AxisEnvFrame(self.axis_name, axis_size, self.main)
    frame = core.axis_frame(self.axis_name, self.main)
    assert axis_size is None or axis_size == frame.size, (axis_size, frame.size)
    assert frame.main_trace is self.main
    return frame

  def process_primitive(self, primitive, tracers, params):
    if config.dynamic_shapes.value:
      primitive.abstract_eval(*(t.aval for t in tracers), **params)
    vals_in, dims_in = unzip2((t.val, t.batch_dim) for t in tracers)
    is_axis_primitive = primitive in axis_primitive_batchers
    used_names = core.used_axis_names(primitive, params)
    if is_axis_primitive and _main_trace_for_axis_names(self.main, used_names):
      frame = self.get_frame(vals_in, dims_in)
      batcher_primitive = self.get_axis_primitive_batcher(primitive, frame)
      val_out, dim_out = batcher_primitive(vals_in, dims_in, **params)
    elif all(bdim is not_mapped for bdim in dims_in):
      return primitive.bind(*vals_in, **params)
    else:
      frame = self.get_frame(vals_in, dims_in)
      batched_primitive = self.get_primitive_batcher(primitive, frame)
      val_out, dim_out = batched_primitive(vals_in, dims_in, **params)
    src = source_info_util.current()
    if primitive.multiple_results:
      return [BatchTracer(self, x, d, src) for x, d in zip(val_out, dim_out)]
    else:
      return BatchTracer(self, val_out, dim_out, src)

  def process_call(self, call_primitive, f, tracers, params):
    assert call_primitive.multiple_results
    params = dict(params, name=params.get('name', f.__name__))
    vals, dims = unzip2((t.val, t.batch_dim) for t in tracers)
    if all(bdim is not_mapped for bdim in dims):
      return call_primitive.bind(f, *vals, **params)
    sizes = (x.shape[d] if type(d) is int else len(d.segment_lengths)
             for x, d in zip(vals, dims) if d is not not_mapped)
    axis_size, = core.dedup_referents(sizes)
    segment_lens, dims = indirectify_ragged_axes(dims)
    f_, dims_out = batch_subtrace(f, self.main, tuple(dims))
    f_ = _update_annotation(
        f_, f.in_type, axis_size, self.axis_name, dims, segment_lens)
    vals_out = call_primitive.bind(f_, *segment_lens, *vals, **params)
    vals_out, dims_out = resolve_ragged_axes(vals_out, dims_out())
    src = source_info_util.current()
    return [BatchTracer(self, v, d, src) for v, d in zip(vals_out, dims_out)]

  def post_process_call(self, call_primitive, out_tracers, params):
    vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info)
                              for t in out_tracers)
    main = self.main
    def todo(vals):
      trace = main.with_cur_sublevel()
      return map(partial(BatchTracer, trace), vals, dims, srcs)
    return vals, todo

  def process_map(self, map_primitive, f: lu.WrappedFun, tracers, params):
    vals, dims = unzip2((t.val, t.batch_dim) for t in tracers)
    if all(dim is not_mapped for dim in dims):
      return map_primitive.bind(f, *vals, **params)
    else:
      assert len({x.shape[d] for x, d in zip(vals, dims) if d is not not_mapped}) == 1
      # The logic for the dimension math below is as follows:
      # ╔═════════════╦════════════════════════════════════════╦═══════════╗
      # ║ d / in_axis ║ None                                   ║ int       ║
      # ╠═════════════╬════════════════════════════════════════╩═══════════╣
      # ║ None        ║ No extra axis, so in_axis unaffected               ║
      # ╠═════════════╬════════════════════════════════════════╦═══════════╣
      # ║ int         ║ Not mapped, so batching dim unaffected ║ See below ║
      # ╚═════════════╩════════════════════════════════════════╩═══════════╝
      # When both d and in_axis are defined then:
      # - If `d <= in_axis`, we have to move the `in_axis` one dimension further;
      # - If `d >  in_axis`, we have to decrement `d` (as `in_axis` will get removed).
      def both_mapped(in_out_axis, d):
        return in_out_axis is not None and d is not not_mapped
      new_in_axes = tuple(
        in_axis + 1 if both_mapped(in_axis, d) and d <= in_axis else in_axis
        for d, in_axis in zip(dims, params['in_axes']))
      new_dims = tuple(
        d - 1 if both_mapped(in_axis, d) and in_axis < d else d
        for d, in_axis in zip(dims, params['in_axes']))
      f, dims_out = batch_subtrace(f, self.main, new_dims)
      out_axes_thunk = params['out_axes_thunk']
      # NOTE: This assumes that the choice of the dimensions over which outputs
      #       are batched is entirely dependent on the function and not e.g. on the
      #       data or its shapes.
      @as_hashable_function(closure=out_axes_thunk)
      def new_out_axes_thunk():
        return tuple(out_axis + 1 if both_mapped(out_axis, d) and d < out_axis else out_axis
                     for out_axis, d in zip(out_axes_thunk(), dims_out()))
      new_params = dict(params, in_axes=new_in_axes, out_axes_thunk=new_out_axes_thunk)
      vals_out = map_primitive.bind(f, *vals, **new_params)
      dims_out_ = [d + 1 if both_mapped(out_axis, d) and out_axis <= d else d
                   for d, out_axis in zip(dims_out(), out_axes_thunk())]
      src = source_info_util.current()
      return [BatchTracer(self, v, d, src) for v, d in zip(vals_out, dims_out_)]

  def post_process_map(self, call_primitive, out_tracers, params):
    vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info)
                              for t in out_tracers)
    main = self.main
    def both_mapped(in_out_axis, d):
      return in_out_axis is not None and d is not not_mapped
    def todo(vals):
      trace = main.with_cur_sublevel()
      return [BatchTracer(trace, v, d + 1 if both_mapped(oa, d) and oa <= d else d, s)
              for v, d, oa, s in zip(vals, dims, params['out_axes_thunk'](), srcs)]
    if call_primitive.map_primitive:
      def out_axes_transform(out_axes):
        return tuple(out_axis + 1 if both_mapped(out_axis, d) and d < out_axis else out_axis
                     for out_axis, d in zip(out_axes, dims))
      todo = (todo, out_axes_transform)
    return vals, todo

  def process_custom_jvp_call(self, prim, fun, jvp, tracers, *, symbolic_zeros):
    in_vals, in_dims = unzip2((t.val, t.batch_dim) for t in tracers)
    fun, out_dims1 = batch_subtrace(fun, self.main, in_dims)
    jvp, out_dims2 = batch_custom_jvp_subtrace(jvp, self.main, in_dims)
    out_vals = prim.bind(fun, jvp, *in_vals, symbolic_zeros=symbolic_zeros)
    fst, out_dims = lu.merge_linear_aux(out_dims1, out_dims2)
    if not fst:
      assert out_dims == out_dims[:len(out_dims) // 2] * 2
      out_dims = out_dims[:len(out_dims) // 2]
    src = source_info_util.current()
    return [BatchTracer(self, v, d, src) for v, d in zip(out_vals, out_dims)]

  def post_process_custom_jvp_call(self, out_tracers, jvp_was_run):
    vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info)
                              for t in out_tracers)
    main = self.main
    def todo(vals):
      trace = main.with_cur_sublevel()
      if jvp_was_run:
        primal_dims, tangent_dims = dims[:len(vals)], dims[len(vals):]
        assert primal_dims == tangent_dims
        primal_srcs = srcs[:len(vals)]
        return map(partial(BatchTracer, trace), vals, primal_dims, primal_srcs)
      else:
        return map(partial(BatchTracer, trace), vals, dims, srcs)
    return vals, todo

  def process_custom_vjp_call(self, prim, fun, fwd, bwd, tracers, *, out_trees,
                              symbolic_zeros):  # pytype: disable=signature-mismatch
    in_vals, in_dims = unzip2((t.val, t.batch_dim) for t in tracers)
    axis_size, = {x.shape[d] for x, d in zip(in_vals, in_dims)
                  if d is not not_mapped}
    fwd_in_dims = [d for in_dim in in_dims for d in [in_dim, not_mapped]]
    fun, out_dims1 = batch_subtrace(fun, self.main, in_dims)
    fwd, out_dims2 = batch_subtrace(fwd, self.main, fwd_in_dims)
    bwd = batch_custom_vjp_bwd(bwd, self.axis_name, axis_size,
                               out_dims2, in_dims, self.main.trace_type,
                               self.spmd_axis_name)
    out_vals = prim.bind(fun, fwd, bwd, *in_vals, out_trees=out_trees,
                         symbolic_zeros=symbolic_zeros)
    fst, out_dims = lu.merge_linear_aux(out_dims1, out_dims2)
    if not fst:
      _, res_tree = out_trees()
      _, out_dims = split_list(out_dims, [res_tree.num_leaves])
    src = source_info_util.current()
    return [BatchTracer(self, v, d, src) for v, d in zip(out_vals, out_dims)]

  def post_process_custom_vjp_call(self, out_tracers, _):
    vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info)
                              for t in out_tracers)
    main = self.main
    def todo(vals):
      trace = main.with_cur_sublevel()
      return map(partial(BatchTracer, trace), vals, dims, srcs)
    return vals, todo

  def post_process_custom_vjp_call_fwd(self, out_tracers, out_trees):
    vals, dims, srcs = unzip3((t.val, t.batch_dim, t.source_info)
                              for t in out_tracers)
    axis_size, = {x.shape[d] for x, d in zip(vals, dims) if d is not not_mapped}
    main, trace_type = self.main, self.main.trace_type
    axis_name = self.axis_name
    _, res_tree = out_trees()
    num_res = res_tree.num_leaves
    res_dims, primal_dims = split_list(dims, [num_res])
    _, primal_srcs = split_list(srcs, [num_res])
    def todo(vals):
      trace = main.with_cur_sublevel()
      return map(partial(BatchTracer, trace), vals, primal_dims, primal_srcs)
    def bwd_transform(bwd):
      return batch_custom_vjp_bwd(bwd, axis_name, axis_size, dims, (None,),
                                  trace_type, self.spmd_axis_name)
    return vals, todo, bwd_transform
