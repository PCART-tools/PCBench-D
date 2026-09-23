def _ensure_spmd_and(f):
  def update(v):
    if v and not SPMD_LOWERING.value:
      raise RuntimeError("This flag requires enabling the experimental_xmap_spmd_lowering flag")
    return f(v)
  return update
