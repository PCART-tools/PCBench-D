def _threefry2x32_abstract_eval(*args):
  if any(a.dtype != jnp.uint32 for a in args):
    raise TypeError("Arguments to threefry2x32 must have uint32 type, got {}"
                    .format(args))
  if all(isinstance(arg, core.ShapedArray) for arg in args):
    shape = lax_internal.broadcasting_shape_rule(*args)
    named_shape = core.join_named_shapes(*(a.named_shape for a in args))
    aval = core.ShapedArray(shape, jnp.dtype(jnp.uint32), named_shape=named_shape)
  else:
    aval = core.UnshapedArray(jnp.dtype(jnp.uint32))
  return (aval,) * 2
