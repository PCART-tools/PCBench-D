def _xla_call_impl(fun: lu.WrappedFun, *args, device, backend, name,
                   donated_invars, inline, keep_unused: bool):
  del inline  # Only used at tracing time
  if fun.in_type is None:
    arg_specs = unsafe_map(arg_spec, args)
  else:
    arg_specs = [(None, getattr(x, '_device', None)) for x in args]
  compiled_fun = xla_callable(fun, device, backend, name, donated_invars,
                              keep_unused, *arg_specs)
  try:
    return compiled_fun(*args)
  except FloatingPointError:
    assert config.jax_debug_nans or config.jax_debug_infs  # compiled_fun can only raise in this case
    print("Invalid value encountered in the output of a jit-decorated function. "
          "Calling the de-optimized version.")
    # We want to run the wrapped function again (after xla_callable already ran
    # it), but linear_util.WrappedFun instances are meant to be run only once.
    # In addition to re-executing the Python code, which is usually undesirable
    # but which config.jax_debug_nans is meant to opt into, we'll be
    # re-executing any linear_util.py-style side effects, i.e. re-populating
    # Stores created by any transformation_with_aux's applied to fun. Since this
    # is intentional here, to avoid "Store occupied" errors we clone the
    # WrappedFun with empty stores.
    stores = [lu.Store() for _ in fun.stores]
    clone = lu.WrappedFun(fun.f, fun.transforms, stores, fun.params,
                          fun.in_type)

    with core.new_sublevel():
      _ = clone.call_wrapped(*args)  # may raise, not return

    # If control reaches this line, we got a NaN on the output of `compiled_fun`
    # but not `clone.call_wrapped` on the same arguments. Let's tell the user.
    fun_info = pe.fun_sourceinfo(fun.f)
    msg = ("An invalid value was encountered in the output of the "
           f"`jit`-decorated function {fun_info}. Because "
           "config.jax_debug_nans and/or config.jax_debug_infs is set, the "
           "de-optimized function (i.e., the function as if the `jit` "
           "decorator were removed) was called in an attempt to get a more "
           "precise error message. However, the de-optimized function did not "
           "produce invalid values during its execution. This behavior can "
           "result from `jit` optimizations causing the invalud value to be "
           "produced. It may also arise from having nan/inf constants as "
           "outputs, like `jax.jit(lambda ...: jax.numpy.nan)(...)`. "
           "\n\n"
           "It may be possible to avoid the invalid value by removing the "
           "`jit` decorator, at the cost of losing optimizations. "
           "\n\n"
           "If you see this error, consider opening a bug report at "
           "https://github.com/google/jax.")
    raise FloatingPointError(msg)
