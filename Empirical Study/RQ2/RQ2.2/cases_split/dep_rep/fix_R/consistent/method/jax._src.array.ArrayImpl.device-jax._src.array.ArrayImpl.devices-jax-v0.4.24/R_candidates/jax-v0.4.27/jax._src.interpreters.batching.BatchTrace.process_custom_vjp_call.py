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
