class CheckifyTrace(core.Trace):
  pure = lift = lambda self, val: CheckifyTracer(self, val)

  def __init__(self, main: core.MainTrace, sublevel: core.Sublevel,
               enabled_errors: FrozenSet['ErrorCategory']) -> None:
    self.main = main
    self.level = main.level
    self.sublevel = sublevel
    self.main.enabled_errors = enabled_errors

  def sublift(self, tracer):
    return CheckifyTracer(self, tracer.val)

  def process_primitive(self, primitive, tracers, params):
    in_vals = [t.val for t in tracers]
    rule = error_checks.get(primitive)
    if rule:
      out, self.main.error = rule(self.main.error, self.main.enabled_errors,  # type: ignore
                                  *in_vals, **params)
    else:
      out = primitive.bind(*in_vals, **params)
    if primitive.multiple_results:
      return [CheckifyTracer(self, x) for x in out]
    else:
      return CheckifyTracer(self, out)

  def process_call(self, primitive, f, tracers, params):
    in_vals = [t.val for t in tracers]
    e = popattr(self.main, 'error')
    f, msgs = checkify_subtrace(f, self.main, tuple(e.msgs.items()))
    if 'donated_invars' in params:
      params = dict(params, donated_invars=(False, False, False,
                                            *params['donated_invars']))
    err, code, payload, *out_vals = primitive.bind(f, e.err, e.code, e.payload,
                                                   *in_vals, **params)
    setnewattr(self.main, 'error', Error(err, code, msgs(), payload))
    return [CheckifyTracer(self, x) for x in out_vals]

  def process_map(self, primitive, f, tracers, params):
    in_vals = [t.val for t in tracers]
    e = popattr(self.main, 'error')
    f, msgs = checkify_subtrace(f, self.main, tuple(e.msgs.items()))

    @as_hashable_function(closure=params['out_axes_thunk'])
    def new_out_axes_thunk():
      return (0, 0, 0, *params['out_axes_thunk']())

    params_ = dict(params, in_axes=(None, None, None, *params['in_axes']),
                   out_axes_thunk=new_out_axes_thunk,
                   donated_invars=(False, False, False, *params['donated_invars']))
    errs, codes, payloads, *outs = primitive.bind(f, e.err, e.code, e.payload,
                                                  *in_vals, **params_)
    err, code, payload = _reduce_any_error(errs, codes, payloads)
    setnewattr(self.main, 'error', Error(err, code, msgs(), payload))
    return [CheckifyTracer(self, x) for x in outs]

  def post_process_call(self, primitive, tracers, params):
    vals = [t.val for t in tracers]
    main = self.main
    e = popattr(main, 'error')
    err, code, payload, main.msgs = e.err, e.code, e.payload, e.msgs
    def todo(vals):
      err, code, payload, *vals = vals
      setnewattr(main, 'error', Error(err, code, popattr(main, 'msgs'), payload))
      trace = main.with_cur_sublevel()
      return [CheckifyTracer(trace, x) for x in vals]
    return (err, code, payload, *vals), todo

  def post_process_map(self, primitive, tracers, params):
    vals = [t.val for t in tracers]
    main = self.main
    e = popattr(main, 'error')
    err, code, payload, main.msgs = e.err, e.code, e.payload, e.msgs
    def todo(vals):
      errs, codes, payloads, *vals = vals
      err, code, payload = _reduce_any_error(errs, codes, payloads)
      setnewattr(main, 'error', Error(err, code, popattr(main, 'msgs'), payload))
      trace = main.with_cur_sublevel()
      return [CheckifyTracer(trace, x) for x in vals]
    def out_axes_transform(out_axes):
      return (0, 0, 0, *out_axes)
    return (err, code, payload, *vals), (todo, out_axes_transform)

  def process_custom_jvp_call(self, prim, fun, jvp, tracers):
    in_vals = [t.val for t in tracers]
    e = popattr(self.main, 'error')
    msgs = tuple(e.msgs.items())
    fun, msgs1 = checkify_subtrace(fun, self.main, msgs)
    jvp, msgs2 = checkify_custom_jvp_subtrace(jvp, self.main, msgs)
    err, code, payload, *out_vals = prim.bind(fun, jvp, e.err, e.code,
                                              e.payload, *in_vals)
    fst, out_msgs = lu.merge_linear_aux(msgs1, msgs2)
    setattr(self.main, 'error', Error(err, code, out_msgs, payload))
    return [CheckifyTracer(self, x) for x in out_vals]

  def post_process_custom_jvp_call(self, out_tracers, jvp_was_run):
    if jvp_was_run:
      msg = ("support for custom_jvp rules which close over checkify values is "
             "not implemented. If you see this, open an issue at "
             "https://github.com/google/jax/issues!")
      raise NotImplementedError(msg)
    vals = [t.val for t in out_tracers]
    main = self.main
    e = popattr(main, 'error')
    err, code, payload, main.msgs = e.err, e.code, e.payload, e.msgs
    def todo(vals):
      err, code, payload, *vals = vals
      setnewattr(main, 'error', Error(err, code, popattr(main, 'msgs'), payload))
      trace = main.with_cur_sublevel()
      return [CheckifyTracer(trace, x) for x in vals]
    return (err, code, payload, *vals), todo

  def process_custom_vjp_call(self, prim, fun, fwd, bwd, tracers, out_trees):
    in_vals = [t.val for t in tracers]
    e = popattr(self.main, 'error')
    msgs = tuple(e.msgs.items())
    fun, msgs1 = checkify_subtrace(fun, self.main, msgs)
    fwd, msgs2 = checkify_custom_vjp_subtrace(fwd, self.main, msgs)
    out = prim.bind(fun, fwd, bwd, e.err, e.code, e.payload,
                    *in_vals, out_trees=out_trees)
    fst, out_msgs = lu.merge_linear_aux(msgs1, msgs2)
    if fst:
      err, code, payload, *out = out
    else:
      err, code, payload = e.err, e.code, e.payload  # forward input error values to output
    setattr(self.main, 'error', Error(err, code, out_msgs, payload))
    return [CheckifyTracer(self, x) for x in out]
