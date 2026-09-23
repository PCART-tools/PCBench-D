def categorical(key: KeyArray,
                logits: RealArray,
                axis: int = -1,
                shape: Optional[Shape] = None) -> Array:
  """Sample random values from categorical distributions.

  Args:
    key: a PRNG key used as the random key.
    logits: Unnormalized log probabilities of the categorical distribution(s) to sample from,
      so that `softmax(logits, axis)` gives the corresponding probabilities.
    axis: Axis along which logits belong to the same categorical distribution.
    shape: Optional, a tuple of nonnegative integers representing the result shape.
      Must be broadcast-compatible with ``np.delete(logits.shape, axis)``.
      The default (None) produces a result shape equal to ``np.delete(logits.shape, axis)``.

  Returns:
    A random array with int dtype and shape given by ``shape`` if ``shape``
    is not None, or else ``np.delete(logits.shape, axis)``.
  """
  key, _ = _check_prng_key(key)
  _check_arraylike("categorical", logits)
  logits_arr = jnp.asarray(logits)

  if axis >= 0:
    axis -= len(logits_arr.shape)

  batch_shape = tuple(np.delete(logits_arr.shape, axis))
  if shape is None:
    shape = batch_shape
  else:
    shape = tuple(shape)
    _check_shape("categorical", shape, batch_shape)

  shape_prefix = shape[:len(shape)-len(batch_shape)]
  logits_shape = list(shape[len(shape) - len(batch_shape):])
  logits_shape.insert(axis % len(logits_arr.shape), logits_arr.shape[axis])
  return jnp.argmax(
      gumbel(key, (*shape_prefix, *logits_shape), logits_arr.dtype) +
      lax.expand_dims(logits_arr, tuple(range(len(shape_prefix)))),
      axis=axis)
