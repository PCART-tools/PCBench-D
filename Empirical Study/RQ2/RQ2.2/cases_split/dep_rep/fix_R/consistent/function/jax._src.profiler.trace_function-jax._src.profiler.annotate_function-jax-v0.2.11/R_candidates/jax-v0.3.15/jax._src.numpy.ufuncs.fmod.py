@_wraps(np.fmod, module='numpy')
@jit
def fmod(x1, x2):
  _check_arraylike("fmod", x1, x2)
  if dtypes.issubdtype(dtypes.result_type(x1, x2), np.integer):
    x2 = _where(x2 == 0, lax_internal._ones(x2), x2)
  return lax.rem(*_promote_args("fmod", x1, x2))
