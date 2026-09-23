def __array_module__(self, types):
  if builtins.all(issubclass(t, _HANDLED_ARRAY_TYPES) for t in types):
    return jax.numpy
  else:
    return NotImplemented
