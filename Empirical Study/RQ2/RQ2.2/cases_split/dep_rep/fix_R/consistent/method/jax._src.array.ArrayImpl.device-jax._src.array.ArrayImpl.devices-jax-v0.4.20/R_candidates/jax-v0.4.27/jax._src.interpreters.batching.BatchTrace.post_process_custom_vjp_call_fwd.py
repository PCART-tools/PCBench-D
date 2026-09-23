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
