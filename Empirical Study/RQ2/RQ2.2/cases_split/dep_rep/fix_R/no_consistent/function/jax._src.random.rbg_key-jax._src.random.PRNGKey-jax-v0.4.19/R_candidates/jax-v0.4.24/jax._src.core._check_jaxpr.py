def _check_jaxpr(
    ctx_factory: Callable[[], tuple[JaxprPpContext, JaxprPpSettings]],
    jaxpr: Jaxpr
  ) -> None:
  # Use set of variables to types to check that variables are in scope.
  env: set[Var] = set()

  def read(x: Atom) -> Atom:
    # Check the type annotation is itself well-typed.
    check_type(ctx_factory, env, x.aval)
    if isinstance(x, Var):
      # Check the variable is in-scope and consistently typed.
      if x not in env:
        ctx, _ = ctx_factory()
        raise JaxprTypeError(f"Variable '{pp_var(x, ctx)}' not defined")
      return x
    elif isinstance(x, Literal):
      # Check that the literal matches its type annotation.
      if not typecheck(x.aval, x.val):
        ctx, _ = ctx_factory()
        raise JaxprTypeError(
            f"Literal value {x.val} does not match its type annotation "
            f"{pp_aval(x.aval, ctx)}")
      return x
    else:
      assert False, "syntactically invalid jaxpr"

  def write(v: Var, a: AbstractValue) -> None:
    assert isinstance(v, Var), "syntactically invalid jaxpr"
    # Check the type annotation of the binder is itself well-typed.
    check_type(ctx_factory, env, v.aval)
    # Check that the variable is not already bound.
    if v in env:
      ctx, _ = ctx_factory()
      raise JaxprTypeError(f"Variable '{pp_var(v, ctx)}' already bound")
    # Check that the computed type is consistent with the binder annotation.
    if not typematch(v.aval, a):
      ctx, _ = ctx_factory()
      raise JaxprTypeError(
          f"Value for variable '{pp_var(v, ctx)}' inconsistently typed "
          f"as {pp_aval(a, ctx)} for let-binder of type {pp_aval(v.aval, ctx)}")
    # If the variable is not a DropVar, add it to the environment.
    if not isinstance(v, DropVar):
      env.add(v)

  # Check type annotations on lambda binders.
  for v in it.chain(jaxpr.constvars, jaxpr.invars):
    check_type(ctx_factory, env, v.aval)
    write(v, v.aval)

  # Check each eqn.
  for eqn_idx, eqn in enumerate(jaxpr.eqns):
    prim = eqn.primitive
    try:
      in_atoms = map(read, eqn.invars)
      in_avals = [x.aval for x in in_atoms]  # use in_atoms for dyn shapes

      # Compute the type of the primitive application.
      if prim in custom_typechecks:
        out_type, eqn_effects = custom_typechecks[prim](
          ctx_factory, *in_atoms, **eqn.params)
      elif prim.call_primitive:
        out_type, eqn_effects = _check_call(ctx_factory, prim, in_atoms,
                                            eqn.params)
      elif prim.map_primitive:
        out_type, eqn_effects = _check_map(ctx_factory, prim, in_avals,
                                           eqn.params)
      else:
        out_type, eqn_effects = check_eqn(prim, in_avals, eqn.params)

      # Check the computed effect type matches the eqn's annotation, and is
      # included in the jaxpr's annotation.
      if eqn.effects != eqn_effects:
        raise JaxprTypeError("Inferred effects do not match equation effects. "
                             f"Equation effects: {eqn.effects}. "
                             f"Inferred effects: {eqn_effects}")
      for eff in eqn.effects:
        if isinstance(eff, effects.JaxprInputEffect):
          eqn_invar = eqn.invars[eff.input_index]
          all_vars = [*jaxpr.constvars, *jaxpr.invars]
          if eqn_invar not in all_vars:
            raise JaxprTypeError(
                "Invalid `JaxprInputEffect`: must correspond to a jaxpr invar")
          jaxpr_index = all_vars.index(eqn_invar)
          jaxpr_effect = eff.replace(input_index=jaxpr_index)
          if jaxpr_effect not in jaxpr.effects:
            raise JaxprTypeError(
                "Invalid `JaxprInputEffect`: must be present in jaxpr. "
                f"{jaxpr_effect} is not in {jaxpr.effects}.")
        elif eff not in jaxpr.effects:
          raise JaxprTypeError("Equation effect not present in jaxpr effects. "
                               f"Equation effect: {eff}. "
                               f"Jaxpr effects: {jaxpr.effects}")

      # Check out_type matches the let-binders' annotation (after substitution).
      out_type = substitute_vars_in_output_ty(out_type, eqn.invars, eqn.outvars)
      map(write, eqn.outvars, out_type)

    except JaxprTypeError as e:
      ctx, settings = ctx_factory()
      msg, = e.args
      src = source_info_util.summarize(eqn.source_info)
      msg = "\n\n".join([msg, "in equation:", str(pp.nest(2, pp_eqn(eqn, ctx, settings))),
                         f"from source: {src}"])
      raise JaxprTypeError(msg, eqn_idx) from None

  # TODO(mattjj): include output type annotation on jaxpr and check it here
  map(read, jaxpr.outvars)
