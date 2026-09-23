def move_binders_to_back(closed_jaxpr: ClosedJaxpr, to_move: Sequence[bool]
                         ) -> ClosedJaxpr:
  """Reorder `invars` by moving those indicated in `to_move` to the back."""
  return move_binders_to_front(closed_jaxpr, map(op.not_, to_move))
