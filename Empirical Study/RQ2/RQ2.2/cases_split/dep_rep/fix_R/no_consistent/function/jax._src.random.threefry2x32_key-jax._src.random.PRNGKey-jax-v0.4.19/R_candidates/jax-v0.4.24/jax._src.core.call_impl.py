def call_impl(f: lu.WrappedFun, *args, **params):
  del params  # params parameterize the call primitive, not the function
  with new_sublevel():
    return f.call_wrapped(*args)
