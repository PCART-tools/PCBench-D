def dot_with_no_batch_dims(prim, *_, **params) -> bool:
  # This is a useful heuristic for transformers.
  if prim is jax._src.lax.lax.dot_general_p:
    (_, _), (lhs_b, rhs_b) = params['dimension_numbers']
    if not lhs_b and not rhs_b:
      return True
  return False
