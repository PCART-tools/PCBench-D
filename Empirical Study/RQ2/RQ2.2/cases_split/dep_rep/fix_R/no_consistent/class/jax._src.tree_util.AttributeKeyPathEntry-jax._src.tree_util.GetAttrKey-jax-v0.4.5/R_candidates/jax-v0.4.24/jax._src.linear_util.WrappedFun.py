class WrappedFun:
  """Represents a function `f` to which `transforms` are to be applied.

  Args:
    f: the function to be transformed.
    transforms: a list of `(gen, gen_static_args)` tuples representing
      transformations to apply to `f.` Here `gen` is a generator function and
      `gen_static_args` is a tuple of static arguments for the generator. See
      description at the start of this module for the expected behavior of the
      generator.
    stores: a list of out_store for the auxiliary output of the `transforms`.
    params: extra parameters to pass as keyword arguments to `f`, along with the
      transformed keyword arguments.
  """
  __slots__ = ("f", "transforms", "stores", "params", "in_type", "debug_info")

  def __init__(self, f, transforms, stores, params, in_type, debug_info):
    self.f = f
    self.transforms = transforms
    self.stores = stores
    self.params = params
    self.in_type = in_type
    self.debug_info = debug_info

  @property
  def __name__(self):
    return getattr(self.f, '__name__', '<unnamed wrapped function>')

  def wrap(self, gen, gen_static_args, out_store) -> WrappedFun:
    """Add another transform and its store."""
    return WrappedFun(self.f, ((gen, gen_static_args),) + self.transforms,
                      (out_store,) + self.stores, self.params, None, None)

  def populate_stores(self, stores):
    """Copy the values from the `stores` into `self.stores`."""
    for self_store, other_store in zip(self.stores, stores):
      if self_store is not None:
        self_store.store(other_store.val)

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

  def __repr__(self):
    def transform_to_str(x):
      i, (gen, args) = x
      return f"{i}   : {fun_name(gen)}   {fun_name(args)}"
    transformation_stack = map(transform_to_str, enumerate(self.transforms))
    return "Wrapped function:\n" + '\n'.join(transformation_stack) + '\nCore: ' + fun_name(self.f) + '\n'

  def __hash__(self):
    return hash((self.f, self.transforms, self.params, self.in_type,
                 self.debug_info))

  def __eq__(self, other):
    return (self.f == other.f and self.transforms == other.transforms and
            self.params == other.params and self.in_type == other.in_type and
            self.debug_info == other.debug_info)
