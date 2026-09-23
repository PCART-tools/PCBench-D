@util._wraps(np.bincount, lax_description="""\
Jax adds the optional `length` parameter which specifies the output length, and
defaults to ``x.max() + 1``. It must be specified for bincount to be compiled
with non-static operands. Values larger than the specified length will be discarded.
If `length` is specified, `minlength` will be ignored.

Additionally, while ``np.bincount`` raises an error if the input array contains
negative values, ``jax.numpy.bincount`` clips negative values to zero.
""")
def bincount(x: ArrayLike, weights: ArrayLike | None = None,
             minlength: int = 0, *, length: int | None = None) -> Array:
  util.check_arraylike("bincount", x)
  if not issubdtype(_dtype(x), integer):
    raise TypeError(f"x argument to bincount must have an integer type; got {_dtype(x)}")
  if ndim(x) != 1:
    raise ValueError("only 1-dimensional input supported.")
  minlength = core.concrete_or_error(operator.index, minlength,
      "The error occurred because of argument 'minlength' of jnp.bincount.")
  if length is None:
    x_arr = core.concrete_or_error(asarray, x,
      "The error occurred because of argument 'x' of jnp.bincount. "
      "To avoid this error, pass a static `length` argument.")
    length = max(minlength, x_arr.size and int(x_arr.max()) + 1)
  else:
    length = core.concrete_dim_or_error(length,
        "The error occurred because of argument 'length' of jnp.bincount.")
  if weights is None:
    weights = np.array(1, dtype=int_)
  elif shape(x) != shape(weights):
    raise ValueError("shape of weights must match shape of x.")
  return zeros(length, _dtype(weights)).at[clip(x, 0)].add(weights)
