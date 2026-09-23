def _check_same_dtypes(name, ignore_fp_precision, *ttypes):
  """Check that dtypes agree, possibly ignoring float precision."""
  # the `ignore_fp_precision` flag exists because the XLA shape inference logic
  # allows mixed floating point precision, but the HLO verifier often rejects it
  if any(core.is_opaque_dtype(t) for t in ttypes):
    return  # TODO(mattjj,frostig): do some checking, friend
  types = map(np.dtype, ttypes)  # canonicalize
  if ignore_fp_precision:
    types = [
        np.floating if dtypes.issubdtype(dtype, np.floating)
        else np.complexfloating if dtypes.issubdtype(dtype, np.complexfloating)
        else dtype for dtype in types]
  if len({dtypes.canonicalize_dtype(t) for t in types}) != 1:
    if ignore_fp_precision:
      msg = ("lax.{} requires arguments to have same dtypes up to floating point "
             "precision, got {}.")
    else:
      msg = "lax.{} requires arguments to have the same dtypes, got {}."
    if name in _JNP_FUNCTION_EQUIVALENTS:
      equiv = _JNP_FUNCTION_EQUIVALENTS[name]
      msg += f" (Tip: jnp.{equiv} is a similar function that does automatic type promotion on inputs)."
    raise TypeError(msg.format(name, ", ".join(map(str, types))))
