def apply_primitive(prim, *args, **params):
  """Impl rule that compiles and runs a single primitive 'prim' using XLA."""
  from jax._src import pjit

  try:
    in_avals, in_shardings = util.unzip2([_arg_spec(a) for a in args])
    compiled_fun = xla_primitive_callable(
        prim, in_avals, OrigShardings(in_shardings), **params)
  except pxla.DeviceAssignmentMismatchError as e:
    fails, = e.args
    # TODO(yashkatariya): Thread through a signature_fun via every primitive
    # using apply_primitive so that the error message has the right argument
    # name instead of `args[0]`, etc.
    arg_names = api_util._arg_names(prim.impl, args, {}, (), ())
    msg = pjit._device_assignment_mismatch_error(
        prim.name, fails, args, 'jit', arg_names)
    raise ValueError(msg) from None

  return compiled_fun(*args)
