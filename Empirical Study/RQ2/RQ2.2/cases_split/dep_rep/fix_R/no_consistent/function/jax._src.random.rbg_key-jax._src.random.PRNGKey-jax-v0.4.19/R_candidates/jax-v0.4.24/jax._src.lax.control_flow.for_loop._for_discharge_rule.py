@state_discharge.register_discharge_rule(for_p)
def _for_discharge_rule(in_avals, _, *args: Any, jaxpr: core.Jaxpr,
                        reverse: bool, which_linear: Sequence[bool],
                        nsteps: int, unroll: int
                        ) -> tuple[Sequence[Any | None], Sequence[Any]]:
  out_vals = for_p.bind(*args, jaxpr=jaxpr, reverse=reverse,
                        which_linear=which_linear, nsteps=nsteps,
                        unroll=unroll)
  new_invals = []
  for aval, out_val in zip(in_avals, out_vals):
    new_invals.append(out_val if isinstance(aval, AbstractRef) else None)
  return new_invals, out_vals
