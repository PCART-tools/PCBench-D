def checkify_flat(fun: lu.WrappedFun, enabled_errors: FrozenSet['ErrorCategory'],
                  *args):
  fun, msgs = checkify_subtrace(fun)
  fun = checkify_traceable(fun, tuple(init_error.msgs.items()), enabled_errors)
  err, code, payload, *outvals = fun.call_wrapped(init_error.err,
                                                  init_error.code,
                                                  init_error.payload, *args)
  return (err, code, payload, outvals), msgs()
