class Compiled(Stage):
  """Compiled representation of a function specialized to types/values.

  A compiled computation is associated with an executable and the
  remaining information needed to execute it. It also provides a
  common API for querying properties of compiled computations across
  JAX's various compilation paths and backends.
  """
  __slots__ = ["args_info", "out_tree", "_executable", "_no_kwargs"]

  args_info: Any                # PyTree of ArgInfo
  out_tree: tree_util.PyTreeDef
  _executable: Executable
  _no_kwargs: bool

  def __init__(self, executable, args_info, out_tree, no_kwargs=False):
    self._executable = executable
    self._no_kwargs = no_kwargs
    self.args_info = args_info
    self.out_tree = out_tree
    self._params = CompiledCallParams(self._executable, self._no_kwargs,
                                      self.in_tree, self.out_tree)
    self._call = None

  def as_text(self) -> str | None:
    """A human-readable text representation of this executable.

    Intended for visualization and debugging purposes. This is not a valid nor
    reliable serialization.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    try:
      return self._executable.as_text()
    except NotImplementedError:
      return None

  def cost_analysis(self) -> Any | None:
    """A summary of execution cost estimates.

    Intended for visualization and debugging purposes. The object output by
    this is some simple data structure that can easily be printed or serialized
    (e.g. nested dicts, lists, and tuples with numeric leaves). However, its
    structure can be arbitrary: it may be inconsistent across versions of JAX
    and jaxlib, or even across invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    # TODO(frostig): improve annotation (basic pytree of arbitrary structure)
    try:
      return self._executable.cost_analysis()
    except NotImplementedError:
      return None

  def memory_analysis(self) -> Any | None:
    """A summary of estimated memory requirements.

    Intended for visualization and debugging purposes. The object output by
    this is some simple data structure that can easily be printed or serialized
    (e.g. nested dicts, lists, and tuples with numeric leaves). However, its
    structure can be arbitrary: it may be inconsistent across versions of JAX
    and jaxlib, or even across invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    # TODO(frostig): improve annotation (basic pytree of arbitrary structure)
    try:
      return self._executable.memory_analysis()
    except NotImplementedError:
      return None

  def runtime_executable(self) -> Any | None:
    """An arbitrary object representation of this executable.

    Intended for debugging purposes. This is not valid nor reliable
    serialization. The output has no guarantee of consistency across
    invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    return self._executable.runtime_executable()

  @property
  def input_shardings(self):  # PyTree[sharding.XLACompatibleSharding]
    shardings_flat = self._executable.input_shardings()
    return tree_util.tree_unflatten(self.in_tree, shardings_flat)  # pytype: disable=attribute-error

  @property
  def output_shardings(self):  # PyTree[sharding.XLACompatibleSharding]
    shardings_flat = self._executable.output_shardings()
    return tree_util.tree_unflatten(self.out_tree, shardings_flat)  # pytype: disable=attribute-error

  def _input_layouts(self):
    layouts_flat = self._executable.input_layouts()
    assert all(isinstance(l, SpecifiedLayout) for l in layouts_flat)
    # Some input layouts got DCE'd
    if self.in_tree.num_leaves > len(layouts_flat):
      iter_layouts_flat = iter(layouts_flat)
      layouts_flat = [next(iter_layouts_flat) if i in self._executable._kept_var_idx
                      else None for i in range(self.in_tree.num_leaves)]
    return tree_util.tree_unflatten(self.in_tree, layouts_flat)  # pytype: disable=attribute-error

  def _output_layouts(self):
    layouts_flat = self._executable.output_layouts()
    assert all(isinstance(l, SpecifiedLayout) for l in layouts_flat)
    return tree_util.tree_unflatten(self.out_tree, layouts_flat)  # pytype: disable=attribute-error

  @staticmethod
  def call(*args, **kwargs):
    # This is because `__call__` passes in `self._params` as the first argument.
    # Instead of making the call signature `call(params, *args, **kwargs)`
    # extract it from args because `params` can be passed as a kwarg by users
    # which might conflict here.
    params = args[0]
    args = args[1:]
    if config.dynamic_shapes.value:
      raise NotImplementedError
    if params.no_kwargs and kwargs:
      kws = ', '.join(kwargs.keys())
      raise NotImplementedError(
          "function was compiled by a transformation that does not support "
          f"keyword arguments, but called with keyword arguments: {kws}")
    args_flat, in_tree = tree_util.tree_flatten((args, kwargs))
    if in_tree != params.in_tree:
      # TODO(frostig): provide more info about the source function
      # and transformation
      raise TypeError(
          f"function compiled for {params.in_tree}, called with {in_tree}")
    try:
      out_flat = params.executable.call(*args_flat)
    except TypeError as e:
      # We can't transform ahead-of-time compiled calls, since we've
      # lowered and compiled for a fixed function signature, and JAX
      # transformations change signatures. We interpret a Tracer
      # argument as an indication of a transformation attempt. We
      # could check this before the executable call, but we'd rather
      # avoid isinstance checks on the call path. Seeing a TypeError
      # might mean that arguments have JAX-invalid types, which in
      # turn might mean some are Tracers.
      for arg in args_flat:
        if isinstance(arg, core.Tracer):
          raise TypeError(
              "Cannot apply JAX transformations to a function lowered and "
              "compiled for a particular signature. Detected argument of "
              f"Tracer type {type(arg)}.") from e
      else:
        raise
    outs = tree_util.tree_unflatten(params.out_tree, out_flat)
    return outs, out_flat, args_flat

  def __call__(self, *args, **kwargs):
    if self._call is None:
      self._call = self._executable.create_cpp_call(
          self._no_kwargs, self.in_tree, self.out_tree)
      if self._call is None:
        params = self._params
        def cpp_call_fallback(*args, **kwargs):
          outs, _, _ = Compiled.call(params, *args, **kwargs)
          return outs
        self._call = cpp_call_fallback
    return self._call(*args, **kwargs)
