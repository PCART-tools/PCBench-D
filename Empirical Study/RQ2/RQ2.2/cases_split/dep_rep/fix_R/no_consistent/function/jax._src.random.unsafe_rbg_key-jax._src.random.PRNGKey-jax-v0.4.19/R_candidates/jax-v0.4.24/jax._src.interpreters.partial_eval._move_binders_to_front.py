@weakref_lru_cache
def _move_binders_to_front(closed_jaxpr: ClosedJaxpr, to_move: tuple[bool, ...]
                           ) -> ClosedJaxpr:
  assert len(closed_jaxpr.in_avals) == len(to_move)
  new_invars = _move_to_front(closed_jaxpr.jaxpr.invars, to_move)
  new_jaxpr = Jaxpr(closed_jaxpr.jaxpr.constvars, new_invars,
                    closed_jaxpr.jaxpr.outvars, closed_jaxpr.jaxpr.eqns,
                    closed_jaxpr.jaxpr.effects)
  new_closed_jaxpr = core.ClosedJaxpr(new_jaxpr, closed_jaxpr.consts)
  return new_closed_jaxpr
