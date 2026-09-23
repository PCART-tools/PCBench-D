def softmax(x: Array,
            axis: Optional[Union[int, tuple[int, ...]]] = -1,
            where: Optional[Array] = None,
            initial: Optional[Array] = None) -> Array:
  r"""Softmax function.

  Computes the function which rescales elements to the range :math:`[0, 1]`
  such that the elements along :code:`axis` sum to :math:`1`.

  .. math ::
    \mathrm{softmax}(x) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}

  Args:
    x : input array
    axis: the axis or axes along which the softmax should be computed. The
      softmax output summed across these dimensions should sum to :math:`1`.
      Either an integer or a tuple of integers.
    where: Elements to include in the :code:`softmax`.
    initial: The minimum value used to shift the input array. Must be present
      when :code:`where` is not None.
  """
  if jax.config.jax_softmax_custom_jvp:
    return _softmax(x, axis, where, initial)
  else:
    return _softmax_deprecated(x, axis, where, initial)
