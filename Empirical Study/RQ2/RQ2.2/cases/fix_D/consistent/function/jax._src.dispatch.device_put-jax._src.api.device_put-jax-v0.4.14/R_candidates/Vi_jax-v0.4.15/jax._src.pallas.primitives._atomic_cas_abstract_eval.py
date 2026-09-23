def _atomic_cas_abstract_eval(ref_aval, cmp_aval, val_aval):
  if cmp_aval.dtype != val_aval.dtype:
    raise ValueError("Dtypes in cmp/val need to match")
  if ref_aval.shape != ():
    raise ValueError("Ref must be scalar.")
  if cmp_aval.shape != ():
    raise ValueError("Cmp must be scalar.")
  if val_aval.shape != ():
    raise ValueError("Val must be scalar.")
  if cmp_aval.shape != val_aval.shape:
    raise ValueError("Dtypes in cmp/val need to match")
  return jax_core.ShapedArray(val_aval.shape, val_aval.dtype), {state.WriteEffect(0)}
