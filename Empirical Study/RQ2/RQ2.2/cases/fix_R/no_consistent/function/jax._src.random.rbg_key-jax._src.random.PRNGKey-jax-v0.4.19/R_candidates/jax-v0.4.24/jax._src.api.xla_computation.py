def xla_computation(fun: Callable,
                    static_argnums: int | Iterable[int] = (),
                    axis_env: Sequence[tuple[AxisName, int]] | None = None,
                    in_parts=None, out_parts=None,
                    backend: str | None = None,
                    tuple_args: bool = False,
                    instantiate_const_outputs: bool | None = None,
                    return_shape: bool = False,
                    donate_argnums: int | Iterable[int] = ()) -> Callable:
  """Creates a function that produces its XLA computation given example args.

  Args:
    fun: Function from which to form XLA computations.
    static_argnums: See the :py:func:`jax.jit` docstring.
    axis_env: Optional, a sequence of pairs where the first element is an axis
      name and the second element is a positive integer representing the size of
      the mapped axis with that name. This parameter is useful when lowering
      functions that involve parallel communication collectives, and it
      specifies the axis name/size environment that would be set up by
      applications of :py:func:`jax.pmap`. See the examples below.
    in_parts: Optional, how each argument to ``fun`` should be partitioned or
      replicated. This is used to specify partitioned XLA computations, see
      ``sharded_jit`` for more info.
    out_parts: Optional, how each output of ``fun`` should be partitioned or
      replicated. This is used to specify partitioned XLA computations, see
      ``sharded_jit`` for more info.
    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.
    tuple_args: Optional bool, defaults to ``False``. If ``True``, the resulting
      XLA computation will have a single tuple argument that is unpacked into
      the specified function arguments. If `None`, tupling will be enabled when
      there are more than 100 arguments, since some platforms have limits on
      argument arity.
    instantiate_const_outputs: Deprecated argument, does nothing.
    return_shape: Optional boolean, defaults to ``False``. If ``True``, the
      wrapped function returns a pair where the first element is the XLA
      computation and the second element is a pytree with the same structure as
      the output of ``fun`` and where the leaves are objects with ``shape``,
      ``dtype``, and ``named_shape`` attributes representing the corresponding
      types of the output leaves.
    donate_argnums: Specify which arguments are "donated" to the computation.
      It is safe to donate arguments if you no longer need them once the
      computation has finished. In some cases XLA can make use of donated
      buffers to reduce the amount of memory needed to perform a computation,
      for example recycling one of your input buffers to store a result. You
      should not reuse buffers that you donate to a computation, JAX will raise
      an error if you try to.

  Returns:
    A wrapped version of ``fun`` that when applied to example arguments returns
    a built XLA Computation (see xla_client.py), from which representations of
    the unoptimized XLA HLO computation can be extracted using methods like
    ``as_hlo_text``, ``as_serialized_hlo_module_proto``, and
    ``as_hlo_dot_graph``. If the argument ``return_shape`` is ``True``, then the
    wrapped function returns a pair where the first element is the XLA
    Computation and the second element is a pytree representing the structure,
    shapes, dtypes, and named shapes of the output of ``fun``.

    Concrete example arguments are not always necessary. For those arguments not
    indicated by ``static_argnums``, any object with ``shape`` and ``dtype``
    attributes is acceptable (excepting namedtuples, which are treated as Python
    containers).

  For example:

  >>> import jax
  >>>
  >>> def f(x): return jax.numpy.sin(jax.numpy.cos(x))
  >>> c = jax.xla_computation(f)(3.)
  >>> print(c.as_hlo_text())  # doctest: +SKIP
  HloModule xla_computation_f.6
  <BLANKLINE>
  ENTRY xla_computation_f.6 {
    constant.2 = pred[] constant(false)
    parameter.1 = f32[] parameter(0)
    cosine.3 = f32[] cosine(parameter.1)
    sine.4 = f32[] sine(cosine.3)
    ROOT tuple.5 = (f32[]) tuple(sine.4)
  }
  <BLANKLINE>
  <BLANKLINE>


  Alternatively, the assignment to ``c`` above could be written:

  >>> import types
  >>> scalar = types.SimpleNamespace(shape=(), dtype=np.dtype(np.float32))
  >>> c = jax.xla_computation(f)(scalar)


  Here's an example that involves a parallel collective and axis name:

  >>> def f(x): return x - jax.lax.psum(x, 'i')
  >>> c = jax.xla_computation(f, axis_env=[('i', 4)])(2)
  >>> print(c.as_hlo_text())  # doctest: +SKIP
  HloModule jaxpr_computation.9
  primitive_computation.3 {
    parameter.4 = s32[] parameter(0)
    parameter.5 = s32[] parameter(1)
    ROOT add.6 = s32[] add(parameter.4, parameter.5)
  }
  ENTRY jaxpr_computation.9 {
    tuple.1 = () tuple()
    parameter.2 = s32[] parameter(0)
    all-reduce.7 = s32[] all-reduce(parameter.2), replica_groups={{0,1,2,3}}, to_apply=primitive_computation.3
    ROOT subtract.8 = s32[] subtract(parameter.2, all-reduce.7)
  }
  <BLANKLINE>
  <BLANKLINE>

  Notice the ``replica_groups`` that were generated. Here's an example that
  generates more interesting ``replica_groups``:

  >>> from jax import lax
  >>> def g(x):
  ...   rowsum = lax.psum(x, 'i')
  ...   colsum = lax.psum(x, 'j')
  ...   allsum = lax.psum(x, ('i', 'j'))
  ...   return rowsum, colsum, allsum
  ...
  >>> axis_env = [('i', 4), ('j', 2)]
  >>> c = xla_computation(g, axis_env=axis_env)(5.)
  >>> print(c.as_hlo_text())  # doctest: +SKIP
  HloModule jaxpr_computation__1.19
  [removed uninteresting text here]
  ENTRY jaxpr_computation__1.19 {
    tuple.1 = () tuple()
    parameter.2 = f32[] parameter(0)
    all-reduce.7 = f32[] all-reduce(parameter.2), replica_groups={{0,2,4,6},{1,3,5,7}}, to_apply=primitive_computation__1.3
    all-reduce.12 = f32[] all-reduce(parameter.2), replica_groups={{0,1},{2,3},{4,5},{6,7}}, to_apply=primitive_computation__1.8
    all-reduce.17 = f32[] all-reduce(parameter.2), replica_groups={{0,1,2,3,4,5,6,7}}, to_apply=primitive_computation__1.13
    ROOT tuple.18 = (f32[], f32[], f32[]) tuple(all-reduce.7, all-reduce.12, all-reduce.17)
  }
  """
  if instantiate_const_outputs is not None:
    raise ValueError(
        "instantiate_const_outputs has been deprecated. Please use the ahead of"
        " time APIs. You can read more here:"
        " https://jax.readthedocs.io/en/latest/aot.html")
  if in_parts is not None:
    raise ValueError(
        "in_parts has been deprecated. Please use the ahead of time APIs. You"
        " can read more here: https://jax.readthedocs.io/en/latest/aot.html")
  if out_parts is not None:
    raise ValueError(
        "out_parts has been deprecated. Please use the ahead of time APIs. You"
        " can read more here: https://jax.readthedocs.io/en/latest/aot.html")

  check_callable(fun)
  static_argnums = _ensure_index_tuple(static_argnums)
  donate_argnums = _ensure_index_tuple(donate_argnums)
  donate_argnums = rebase_donate_argnums(donate_argnums, static_argnums)

  fun_name = getattr(fun, "__name__", "unknown")

  platform = backend if backend is not None else xb.get_backend().platform

  def make_axis_env(nreps):
    if axis_env is None:
      return sharding_impls.AxisEnv(nreps, (), ())
    else:
      nreps = nreps * math.prod(size for name, size in axis_env)
      names, sizes = unzip2(axis_env)
      return sharding_impls.AxisEnv(nreps, names, sizes)

  @wraps(fun)
  @api_boundary
  def computation_maker(*args, **kwargs):
    if max(static_argnums + donate_argnums, default=-1) >= len(args):
      raise ValueError(f"jitted function has {static_argnums=}, {donate_argnums=} but "
                       f"was called with only {len(args)} positional arguments.")

    f = lu.wrap_init(fun)
    f, dyn_args = argnums_partial_except(f, static_argnums, args, allow_invalid=False)
    args_flat, in_tree = tree_flatten((dyn_args, kwargs))
    if donate_argnums:
      donated_invars = donation_vector(donate_argnums, (), dyn_args, kwargs)
    else:
      donated_invars = (False,) * len(args_flat)

    jaxtree_fun, out_tree = flatten_fun(f, in_tree)
    avals = map(shaped_abstractify, args_flat)
    with ExitStack() as stack:
      for axis_name, size in axis_env or []:
        stack.enter_context(core.extend_axis_env(axis_name, size, None))
      jaxpr, out_avals, consts, () = pe.trace_to_jaxpr_dynamic(jaxtree_fun, avals)
      jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)
      axis_env_ = make_axis_env(dispatch.jaxpr_replicas(jaxpr))
      ordered_effects = list(
          effects.ordered_effects.filter_in(jaxpr.effects))
      lowering_result = mlir.lower_jaxpr_to_module(
          f"xla_computation_{fun_name}",
          core.ClosedJaxpr(jaxpr, consts),
          ordered_effects=ordered_effects,
          backend_or_name=backend,
          platforms=[platform],
          axis_context=sharding_impls.ReplicaAxisContext(axis_env_),
          name_stack=source_info_util.new_name_stack(
              wrap_name(fun_name, "xla_computation")),
          donated_args=donated_invars,
          arg_shardings=None,
          result_shardings=None,
          lowering_parameters=mlir.LoweringParameters())
      built = xc._xla.mlir.mlir_module_to_xla_computation(
          mlir.module_to_string(lowering_result.module),
          use_tuple_args=tuple_args,
          return_tuple=True)
    out_shapes_flat = [
        ShapeDtypeStruct(a.shape, a.dtype, a.named_shape) for a in out_avals]
    out_shape = tree_unflatten(out_tree(), out_shapes_flat)
    for out_aval in out_avals:
      if not isinstance(out_aval, ShapedArray):
        raise RuntimeError("As we want to propagate the weak_type, we need "
                           "to get a ShapedArray, otherwise this "
                           "information is lost")

    if return_shape:
      return built, out_shape
    else:
      return built

  return computation_maker
