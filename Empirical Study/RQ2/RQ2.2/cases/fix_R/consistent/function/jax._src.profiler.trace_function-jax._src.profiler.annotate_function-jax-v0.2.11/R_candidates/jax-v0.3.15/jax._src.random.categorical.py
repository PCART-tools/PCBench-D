def categorical(key: KeyArray,
                logits: RealArray,
                axis: int = -1,
                shape: Optional[Sequence[int]] = None) -> jnp.ndarray:
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

  if axis >= 0:
    axis -= len(logits.shape)

  batch_shape = tuple(np.delete(logits.shape, axis))
  if shape is None:
    shape = batch_shape
  else:
    shape = tuple(shape)
    _check_shape("categorical", shape, batch_shape)

  sample_shape = shape[:len(shape)-len(batch_shape)]
  return jnp.argmax(
      gumbel(key, sample_shape + logits.shape, logits.dtype) +
      lax.expand_dims(logits, tuple(range(len(sample_shape)))),
      axis=axis)
