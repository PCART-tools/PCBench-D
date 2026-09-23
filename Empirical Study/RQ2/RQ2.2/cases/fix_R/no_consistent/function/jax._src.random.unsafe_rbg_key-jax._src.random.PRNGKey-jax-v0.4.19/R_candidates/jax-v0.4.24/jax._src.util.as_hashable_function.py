def as_hashable_function(closure):
  return lambda f: HashableFunction(f, closure)
