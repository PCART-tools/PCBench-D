def _sort_abstract_eval(*args, **kwargs):
  args = tuple(raise_to_shaped(arg) for arg in args)
  if any(arg.shape != args[0].shape for arg in args[1:]):
    shapes = " ".join(str(a.shape) for a in args)
    raise TypeError(f"Arguments to sort must have equal shapes, got: {shapes}")
  return args
