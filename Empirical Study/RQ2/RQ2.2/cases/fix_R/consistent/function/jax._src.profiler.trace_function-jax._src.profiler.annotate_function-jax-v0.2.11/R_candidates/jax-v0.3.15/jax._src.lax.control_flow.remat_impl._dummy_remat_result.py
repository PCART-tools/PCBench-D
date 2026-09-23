def _dummy_remat_result(aval: core.AbstractValue):
  """A result that will be discarded"""
  if aval is core.abstract_token:
    return lax.create_token()
  else:
    return lax.broadcast(np.array(0, dtype=aval.dtype), aval.shape)  # type: ignore
