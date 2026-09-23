@partial(jax.jit, static_argnames=("axis",))
def log_softmax(x: Array,
                axis: Optional[Union[int, Tuple[int, ...]]] = -1,
                where: Optional[Array] = None,
                initial: Optional[Array] = None) -> Array:
  r"""Log-Softmax function.

  Computes the logarithm of the :code:`softmax` function, which rescales
  elements to the range :math:`[-\infty, 0)`.

  .. math ::
    \mathrm{log\_softmax}(x) = \log \left( \frac{\exp(x_i)}{\sum_j \exp(x_j)}
    \right)

  Args:
    x : input array
    axis: the axis or axes along which the :code:`log_softmax` should be
      computed. Either an integer or a tuple of integers.
    where: Elements to include in the :code:`log_softmax`.
    initial: The minimum value used to shift the input array. Must be present
      when :code:`where` is not None.
  """
  x_max = jnp.max(x, axis, where=where, initial=initial, keepdims=True)
  shifted = x - lax.stop_gradient(x_max)
  shifted_logsumexp = jnp.log(
      jnp.sum(jnp.exp(shifted), axis, where=where, keepdims=True))
  return shifted - shifted_logsumexp
