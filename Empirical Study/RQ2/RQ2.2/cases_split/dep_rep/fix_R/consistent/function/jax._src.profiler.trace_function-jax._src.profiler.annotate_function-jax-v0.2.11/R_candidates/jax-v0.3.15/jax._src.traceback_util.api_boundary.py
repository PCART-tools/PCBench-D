def api_boundary(fun: C) -> C:
  '''Wraps ``fun`` to form a boundary for filtering exception tracebacks.

  When an exception occurs below ``fun``, this appends to it a custom
  ``__cause__`` that carries a filtered traceback. The traceback imitates the
  stack trace of the original exception, but with JAX-internal frames removed.

  This boundary annotation works in composition with itself. The topmost frame
  corresponding to an ``api_boundary`` is the one below which stack traces are
  filtered. In other words, if ``api_boundary(f)`` calls ``api_boundary(g)``,
  directly or indirectly, the filtered stack trace provided is the same as if
  ``api_boundary(f)`` were to simply call ``g`` instead.

  This annotation is primarily useful in wrapping functions output by JAX's
  transformations. For example, consider ``g = jax.jit(f)``. When ``g`` is
  called, JAX's JIT compilation machinery is invoked, which in turn calls ``f``
  in order to trace and translate it. If the function ``f`` raises an exception,
  the stack unwinds through JAX's JIT internals up to the original call site of
  ``g``. Because the function returned by ``jax.jit`` is annotated as an
  ``api_boundary``, such an exception is accompanied by an additional traceback
  that excludes the frames specific to JAX's implementation.
  '''

  @util.wraps(fun)
  def reraise_with_filtered_traceback(*args, **kwargs):
    __tracebackhide__ = True
    try:
      return fun(*args, **kwargs)
    except Exception as e:
      mode = filtering_mode()
      if is_under_reraiser(e) or mode == "off":
        raise
      if mode == "tracebackhide":
        add_tracebackhide_to_hidden_frames(e.__traceback__)
        raise
      assert mode == "remove_frames", mode

      filtered_tb, unfiltered, mode = None, None, None
      try:
        filtered_tb = filter_traceback(e.__traceback__)
        msg = format_exception_only(e)
        msg = f'{msg}\n\n{_jax_message_append}'
        unfiltered = UnfilteredStackTrace(msg)
        unfiltered.with_traceback(add_call_stack_frames(e.__traceback__))
        unfiltered.__context__ = e.__context__
        unfiltered.__cause__ = e.__cause__
        unfiltered.__suppress_context__ = e.__suppress_context__
        e.__context__ = None
        e.__cause__ = unfiltered

        # There seems to be no way to alter the currently raised exception's
        # traceback, except via the C API. The currently raised exception
        # is part of the interpreter's thread state: value `e` is a copy.
        xla_extension.replace_thread_exc_traceback(filtered_tb)
        raise
      finally:
        del filtered_tb
        del unfiltered
        del mode
  return reraise_with_filtered_traceback
