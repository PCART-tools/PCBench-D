def select(pred: Array, on_true: Array, on_false: Array) -> Array:
  """Wraps XLA's `Select
  <https://www.tensorflow.org/xla/operation_semantics#select>`_
  operator.
  """
  # Caution! The select_n_p primitive has the *opposite* order of arguments to
  # select(). This is because it implements `select_n`.
  return select_n_p.bind(pred, on_false, on_true)
