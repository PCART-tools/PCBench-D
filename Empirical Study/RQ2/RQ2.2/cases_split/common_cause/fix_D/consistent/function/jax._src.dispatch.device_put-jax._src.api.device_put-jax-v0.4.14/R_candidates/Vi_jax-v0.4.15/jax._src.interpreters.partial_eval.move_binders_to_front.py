def move_binders_to_front(closed_jaxpr: ClosedJaxpr, to_move: Sequence[bool]
                          ) -> ClosedJaxpr:
  """Reorder `invars` by moving those indicated in `to_move` to the front."""
  return _move_binders_to_front(closed_jaxpr, tuple(to_move))
