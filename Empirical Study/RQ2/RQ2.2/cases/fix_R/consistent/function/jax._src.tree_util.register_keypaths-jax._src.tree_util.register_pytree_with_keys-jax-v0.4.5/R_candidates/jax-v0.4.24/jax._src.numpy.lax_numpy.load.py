@util.implements(np.load, update_doc=False)
def load(*args: Any, **kwargs: Any) -> Array:
  # The main purpose of this wrapper is to recover bfloat16 data types.
  # Note: this will only work for files created via np.save(), not np.savez().
  out = np.load(*args, **kwargs)
  if isinstance(out, np.ndarray):
    # numpy does not recognize bfloat16, so arrays are serialized as void16
    if out.dtype == 'V2':
      out = out.view(bfloat16)
    try:
      out = asarray(out)
    except (TypeError, AssertionError):  # Unsupported dtype
      pass
  return out
