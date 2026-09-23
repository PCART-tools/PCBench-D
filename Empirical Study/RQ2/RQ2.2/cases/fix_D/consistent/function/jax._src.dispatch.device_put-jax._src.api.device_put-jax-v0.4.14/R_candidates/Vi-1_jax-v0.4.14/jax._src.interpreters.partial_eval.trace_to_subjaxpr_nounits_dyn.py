@lu.transformation_with_aux
def trace_to_subjaxpr_nounits_dyn(
    main: core.MainTrace, in_knowns: Sequence[bool], in_type: InputType,
    instantiate: bool | Sequence[bool],
    *in_consts: Any):
  trace = main.with_cur_sublevel()
  in_avals, which_explicit = unzip2(in_type)

  # To form input tracers from in_type, we need to first build ConstVar tracers
  # for all axis sizes, so that we can then use those tracers in the shapes of
  # avals for unknown inputs' tracers. We use ConstVar recipes for on-the-fly
  # type agreement checking via get_referent.
  in_consts_full: list[JaxprTracer | None] = [None] * len(in_type)
  in_consts_iter, in_knowns_iter = iter(in_consts), iter(in_knowns)
  for idx, (aval, explicit) in enumerate(in_type):
    if explicit and next(in_knowns_iter):
      constval = next(in_consts_iter)
      if isinstance(aval, DShapedArray):
        for i, d in enumerate(aval.shape):
          if isinstance(d, DBIdx):
            if in_consts_full[d.val] is None:
              in_consts_full[d.val] = \
                  JaxprTracer(trace, PartialVal.unknown(in_avals[d.val]),
                              ConstVar(constval.shape[i]))
            assert core.same_referent(constval.shape[i], in_consts_full[d.val])
        shape = [in_consts_full[d.val] if type(d) is DBIdx else d  # type: ignore
                 for d in aval.shape]
        aval = aval.update(shape=tuple(shape))
      in_consts_full[idx] = JaxprTracer(trace, PartialVal.unknown(aval),
                                        ConstVar(constval))
  # Check that we covered all axis sizes with ConstVar tracers.
  for idx, (aval, explicit) in enumerate(in_type):
    if not explicit: assert in_consts_full[idx] is not None
    if isinstance(aval, DShapedArray):
      assert all(type(d) is not DBIdx or in_consts_full[d.val] is not None  # type: ignore
                 for d in aval.shape)

  # Next, build tracers for all unknown inputs, using the in_consts_full list
  # for axis size tracers when necessary.
  in_tracers = []
  in_knowns_iter = iter(in_knowns)
  for aval, explicit in in_type:
    if explicit and not next(in_knowns_iter):
      if isinstance(aval, DShapedArray):
        shape = [in_consts_full[d.val] if type(d) is DBIdx else d  # type: ignore
                 for d in aval.shape]
        aval = aval.update(shape=tuple(shape))
      tracer = JaxprTracer(trace, PartialVal.unknown(aval), LambdaBinding())
      in_tracers.append(tracer)

  # Merge in_consts and in_tracers and call wrapped fn with  explicit arguments.
  in_args = merge_lists(in_knowns, in_tracers, in_consts)
  ans = yield in_args, {}

  # Instantiate outputs and build jaxpr.
  if isinstance(instantiate, bool):
    instantiate = [instantiate] * len(ans)
  out_tracers = map(trace.full_raise, map(core.full_lower, ans))
  out_tracers = [trace.instantiate_const(trace.full_raise(t)) if inst else t
                 for inst, t in zip(instantiate, out_tracers)]

  # Collect known outputs.
  out_knowns: list[bool] = [t.is_known() for t in out_tracers]
  out_consts: list[Any] = [t.pval.get_known() for t in out_tracers
                           if t.is_known()]

  # Build the jaxpr.
  out_tracers = [t for t in out_tracers if not t.is_known()]
  jaxpr, res, env = tracers_to_jaxpr(in_tracers, out_tracers)
  out_avals = [v.aval for v in jaxpr.outvars]
  idx_map = {v: InDBIdx(i)
             for i, v in enumerate(it.chain(jaxpr.constvars, jaxpr.invars))}
  out_type = [(a.update(shape=tuple(idx_map.get(d, d) for d in a.shape))  # type: ignore
               if type(a) is DShapedArray else a, True) for a in out_avals]

  # Which residuals are just forwarded inputs? Check obj id, then prune.
  id_map = {id(c.recipe.val): i for i, c in enumerate(in_consts_full)  # type: ignore
            if c is not None}
  fwds: list[int | None] = [id_map.get(id(c)) for c in res]
  res = tuple([c for c, fwd in zip(res, fwds) if fwd is None])

  del main, in_consts, trace, in_consts_iter, in_knowns_iter, in_consts_full, \
      in_tracers, in_args, ans, out_tracers, out_avals
  yield (*out_consts, *res), (fwds, out_knowns, tuple(out_type), jaxpr, env)
