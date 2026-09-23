def apply_primitive(prim, *args, **params):
  """Impl rule that compiles and runs a single primitive 'prim' using XLA."""
  compiled_fun = xla_primitive_callable(prim, *unsafe_map(arg_spec, args),
                                        **params)
  return compiled_fun(*args)
