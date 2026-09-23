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
