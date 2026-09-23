  def process_custom_transpose(self, prim, call, tracers, **params):
    ps_in, ts_in = unzip2((t.primal, t.tangent) for t in tracers)
    res_ps_in, lin_ps_in = split_list(ps_in, [params['res_tree'].num_leaves])
    res_ts_in, lin_ts_in = split_list(ts_in, [params['res_tree'].num_leaves])

    # TODO(frostig): Handle differentiation with respect to residual
    # operands. Calling `call` twice on all operands invalid, since it
    # isn't linear in the residuals. However, we know that if we
    # write:
    #
    #   jvp_call_res = lambda x: partial(jvp, lambda r: call(r, x))
    #
    # then:
    #
    #   jvp(call, (r, x), (dr, dx)) == jvp_call_res(x)(r, dr) + call(r, dx)
    #
    # In words: a possible strategy is to take the jvp of `call` with
    # respect to residuals, and with linear arguments fixed, then add
    # that to a custom-transpose call to `call` (i.e. what we already
    # do below in the all-linear argument case).

    if any(type(t) is not Zero for t in res_ts_in):
      raise NotImplementedError(
        'JVP of custom transpose with respect to non-symbolic-zero residuals')

    ps_out = prim.bind(call, *ps_in, **params)

    lin_ts_in = map(instantiate_zeros, lin_ts_in)
    ts_out = prim.bind(call, *res_ps_in, *lin_ts_in, **params)

    return map(partial(JVPTracer, self), ps_out, ts_out)
