def is_symbolic_dim(v: Any) -> bool:
  """Checks if a value is a symbolic dimension used for shape polymorphism.

  This should be used very rarely, because symbolic dimensions overload all
  operators, and should just work.
  """
  return hasattr(v, "dimension_as_value")
