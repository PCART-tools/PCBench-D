  def call_wrapped(self, *args, **kwargs):
    """Calls the underlying function, applying the transforms.

    The positional `args` and keyword `kwargs` are passed to the first
    transformation generator.
    """
    stack = []
    for (gen, gen_static_args), out_store in zip(self.transforms, self.stores):
      gen = gen(*(gen_static_args + tuple(args)), **kwargs)
      args, kwargs = next(gen)
      stack.append((gen, out_store))
    gen = gen_static_args = out_store = None

    try:
      ans = self.f(*args, **dict(self.params, **kwargs))
    except:
      # Some transformations yield from inside context managers, so we have to
      # interrupt them before reraising the exception. Otherwise they will only
      # get garbage-collected at some later time, running their cleanup tasks
      # only after this exception is handled, which can corrupt the global
      # state.
      while stack:
        stack.pop()[0].close()
      raise

    args = kwargs = None
    while stack:
      gen, out_store = stack.pop()
      try:
        ans = gen.send(ans)
      except:
        # As above does for the first half of the transformation, exceptions
        # raised in the second half of the transformation also require us to
        # clean up references here.
        while stack:
          stack.pop()[0].close()
        raise
      if out_store is not None:
        ans, side = ans
        out_store.store(side)

    return ans
