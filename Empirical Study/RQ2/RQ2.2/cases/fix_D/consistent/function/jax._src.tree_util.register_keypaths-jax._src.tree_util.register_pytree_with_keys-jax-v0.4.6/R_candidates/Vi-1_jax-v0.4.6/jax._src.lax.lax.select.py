def select(pred: ArrayLike, on_true: ArrayLike, on_false: ArrayLike) -> Array:
  """Selects between two branches based on a boolean predicate.

  Wraps XLA's `Select
  <https://www.tensorflow.org/xla/operation_semantics#select>`_
  operator.

  In general :func:`~jax.lax.select` leads to evaluation of both branches, although
  the compiler may elide computations if possible. For a similar function that
  usually evaluates only a single branch, see :func:`~jax.lax.cond`.

  Args:
    pred: boolean array
    on_true: array containing entries to return where ``pred`` is True. Must have
      the same shape as ``pred``, and the same shape and dtype as ``on_false``.
    on_false: array containing entries to return where ``pred`` is False. Must have
      the same shape as ``pred``, and the same shape and dtype as ``on_true``.

  Returns:
    result: array with same shape and dtype as ``on_true`` and ``on_false``.
  """
  # Caution! The select_n_p primitive has the *opposite* order of arguments to
  # select(). This is because it implements `select_n`.
  return select_n_p.bind(pred, on_false, on_true)
