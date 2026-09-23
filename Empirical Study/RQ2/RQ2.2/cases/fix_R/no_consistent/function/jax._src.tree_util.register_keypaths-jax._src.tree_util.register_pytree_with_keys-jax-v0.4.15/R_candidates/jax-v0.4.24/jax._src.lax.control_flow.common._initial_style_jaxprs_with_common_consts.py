@cache()
def _initial_style_jaxprs_with_common_consts(
    funs: Sequence[Callable], in_tree, in_avals, primitive_name: str):
  # When staging the branches of a conditional into jaxprs, constants are
  # extracted from each branch and converted to jaxpr arguments. To use the
  # staged jaxprs as the branches to a conditional *primitive*, we need for
  # their (input) signatures to match. This function "joins" the staged jaxprs:
  # for each one, it makes another that accepts *all* constants, but only uses
  # those that it needs (dropping the rest).

  jaxpr_data = [_initial_style_open_jaxpr(fn, in_tree, in_avals, primitive_name)
                for fn in funs]
  if not jaxpr_data:
    return [], [], []

  jaxprs, all_consts, all_out_trees, all_attrs_tracked = zip(*jaxpr_data)
  all_const_avals = [map(_abstractify, consts) for consts in all_consts]
  # If we get a `Ref` in the consts, we know it must come from an outer
  # `run_state`. We also know if shouldn't be boxed up in another tracer.
  # We assert that it is in fact a DynamicJaxprTracer
  for consts, consts_avals in zip(all_consts, all_const_avals):
    for c, aval in zip(consts, consts_avals):
      if isinstance(aval, state.AbstractRef):
        assert isinstance(c, pe.DynamicJaxprTracer)

  # TODO(sharadmv,mattjj): we could dedup *all consts* instead of just the Refs.

  # We don't want two different Refs in a jaxpr's input to refer to the same
  # Ref in the caller. We call this the "Ref aliasing problem" and it introduces
  # difficulties when discharging Refs and when reasoning about programs with
  # state effects. When unifying the arguments to each branch in a cond,
  # however, we might naively pass the same Ref in multiple times.
  #
  # Here we dedup any `Ref`s that were closed over across the branches and
  # pad out constants used across different branches.
  # Let's consider an example case. For the following branch jaxprs, we will
  # produce the following const lists, where `t_` indicates a tracer (a Ref).
  # { lambda x:i32[] a:Ref{float64[]} c:Ref[float64[]}; . let
  #    a[] <- 1.0
  #    c[] <- 3.14
  #   in () }

  # { lambda  d:Ref[float64[]} b:Ref{float64[]} y:i32[]; . let
  #     d[] <- 6.28
  #     b[] <- 2.0
  #   in () }
  # consts = [[0, t_e, t_f], [t_g, t_e, 1]]
  #
  # Notice how `t_e` is duplicated. To deduplicate the `Ref`s we first
  # 1) Detecting duplicate `Ref` tracers. We keep track of duplicates in
  #    `tracer_id_to_canonical_id.` We store the deduped `Ref` tracers in a
  #    list called `canonical_refs`. We remove the `Ref`s from the consts.
  #    We should have the following lists:
  #    canonical_refs = [t_e, t_f, t_g]
  #    consts = [[0], [1]]
  # 2) We need to munge the branch jaxprs to take in *all* the canonical Refs
  #    and ignore the ones it doesn't actually use. We do this by keeping track
  #    for each jaxpr for each of its input Refs which canonical_ref it
  #    corresponds to, producing the following list:
  #    canonical_ref_indices = [[0, 1], [2, 0]]
  #
  # Afterwards, we proceed by rewriting the jaxprs to be the following:
  # { lambda a:Ref{float64[]} c:Ref[float64[]} b_:Ref{float64[]} x:i32[]; . let
  #    a[] <- 1.0
  #    c[] <- 3.14
  #   in () }
  # { lambda b:Ref{float64[]} _:Ref{float64[]} d:Ref{float64[]} y:i32[]; . let
  #     d[] <- 6.28
  #     b[] <- 2.0
  #   in () }
  canonical_ref_indices = []
  canonical_refs: list[Any] = []
  tracer_id_to_canonical_id = {}
  all_nonref_consts = []
  canonical_ref_avals = []
  all_nonref_const_avals = []
  for consts, consts_avals in zip(all_consts, all_const_avals):
    ref_indices = []
    nonref_consts = []
    nonref_const_avals = []
    for c, aval in zip(consts, consts_avals):
      if isinstance(aval, state.AbstractRef):
        tracer_id = id(c)
        if tracer_id not in tracer_id_to_canonical_id:
          canonical_id = len(canonical_refs)
          canonical_refs.append(c)
          tracer_id_to_canonical_id[tracer_id] = canonical_id
          canonical_ref_avals.append(aval)
        canonical_id = tracer_id_to_canonical_id[tracer_id]
        ref_indices.append(canonical_id)
      else:
        nonref_consts.append(c)
        nonref_const_avals.append(aval)
    all_nonref_consts.append(nonref_consts)
    all_nonref_const_avals.append(nonref_const_avals)
    canonical_ref_indices.append(ref_indices)

  newvar = core.gensym(jaxprs, suffix='_')
  unused_ref_const_vars = map(newvar, canonical_ref_avals)
  unused_const_vars = [map(newvar, const_avals)
                       for const_avals in all_nonref_const_avals]
  def pad_jaxpr_constvars(i, jaxpr):
    is_ref = [isinstance(v.aval, state.AbstractRef) for v in jaxpr.constvars]
    nonref_constvars, ref_constvars = partition_list(is_ref, jaxpr.constvars)
    padded_ref_constvars = unused_ref_const_vars[:]
    for canonical_id, ref_var in zip(canonical_ref_indices[i], ref_constvars):
      padded_ref_constvars[canonical_id] = ref_var
    const_prefix = util.concatenate(unused_const_vars[:i])
    const_suffix = util.concatenate(unused_const_vars[i + 1:])
    constvars = [*padded_ref_constvars, *const_prefix, *nonref_constvars,
                 *const_suffix]
    jaxpr = jaxpr.replace(constvars=constvars)
    effects = pe.make_jaxpr_effects(jaxpr.constvars, jaxpr.invars,
                                    jaxpr.outvars, jaxpr.eqns)
    jaxpr = jaxpr.replace(effects=effects)
    return jaxpr

  consts = [*canonical_refs, *util.concatenate(all_nonref_consts)]
  jaxprs = tuple(pad_jaxpr_constvars(i, jaxpr) for i, jaxpr in enumerate(jaxprs))
  closed_jaxprs = [core.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr), ())
                   for jaxpr in jaxprs]
  return closed_jaxprs, consts, all_out_trees
