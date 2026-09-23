def dce_jaxpr(jaxpr: Jaxpr, used_outputs: Sequence[bool],
              instantiate: bool | Sequence[bool] = False,
              ) -> tuple[Jaxpr, list[bool]]:
  if type(instantiate) is bool:
    instantiate = (instantiate,) * len(jaxpr.invars)
  return _dce_jaxpr(jaxpr, tuple(used_outputs), tuple(instantiate))
