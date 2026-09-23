def concrete_aval(x):
  for typ in type(x).__mro__:
    handler = pytype_aval_mappings.get(typ)
    if handler: return handler(x)
  if hasattr(x, '__jax_array__'):
    return concrete_aval(x.__jax_array__())
  raise TypeError(f"Value {repr(x)} with type {type(x)} is not a valid JAX "
                   "type")
