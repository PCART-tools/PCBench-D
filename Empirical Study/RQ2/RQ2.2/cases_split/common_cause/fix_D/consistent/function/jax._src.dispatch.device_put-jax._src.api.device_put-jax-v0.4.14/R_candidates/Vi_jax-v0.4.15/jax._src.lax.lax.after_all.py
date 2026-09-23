def after_all(*operands):
  """Merges one or more XLA token values. Experimental.

  Wraps the XLA AfterAll operator."""
  return after_all_p.bind(*operands)
