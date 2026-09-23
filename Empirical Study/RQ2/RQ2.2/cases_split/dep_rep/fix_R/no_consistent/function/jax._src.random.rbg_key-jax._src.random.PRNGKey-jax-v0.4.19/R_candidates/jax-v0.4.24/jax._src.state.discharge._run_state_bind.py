def _run_state_bind(*args: Any, jaxpr: core.Jaxpr,
                    which_linear: tuple[bool, ...]):
  if config.enable_checks.value:
    core.check_jaxpr(jaxpr)
    assert len(jaxpr.invars) == len(args)
    assert len(which_linear) == len(args)
  return core.Primitive.bind(run_state_p, *args, jaxpr=jaxpr,
                             which_linear=which_linear)
