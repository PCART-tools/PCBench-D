@partial(jit, static_argnames=['mode', 'op', 'precision', 'preferred_element_type'])
def _conv(x: Array, y: Array, mode: str, op: str, precision: PrecisionLike,
          preferred_element_type: Optional[DTypeLike] = None) -> Array:
  if ndim(x) != 1 or ndim(y) != 1:
    raise ValueError(f"{op}() only support 1-dimensional inputs.")
  if preferred_element_type is None:
    # if unspecified, promote to inexact following NumPy's default for convolutions.
    x, y = util.promote_dtypes_inexact(x, y)
  else:
    # otherwise cast to same type but otherwise preserve input dtypes
    x, y = util.promote_dtypes(x, y)
  if len(x) == 0 or len(y) == 0:
    raise ValueError(f"{op}: inputs cannot be empty, got shapes {x.shape} and {y.shape}.")

  out_order = slice(None)
  if op == 'correlate':
    y = ufuncs.conj(y)
    if len(x) < len(y):
      x, y = y, x
      out_order = slice(None, None, -1)
  elif op == 'convolve':
    if len(x) < len(y):
      x, y = y, x
    y = flip(y)

  if mode == 'valid':
    padding = [(0, 0)]
  elif mode == 'same':
    padding = [(y.shape[0] // 2, y.shape[0] - y.shape[0] // 2 - 1)]
  elif mode == 'full':
    padding = [(y.shape[0] - 1, y.shape[0] - 1)]
  else:
    raise ValueError("mode must be one of ['full', 'same', 'valid']")

  result = lax.conv_general_dilated(x[None, None, :], y[None, None, :], (1,),
                                    padding, precision=precision,
                                    preferred_element_type=preferred_element_type)
  return result[0, 0, out_order]
