def make_jaxpr(fun: Callable,
               static_argnums: Union[int, Iterable[int]] = (),
               axis_env: Optional[Sequence[Tuple[AxisName, int]]] = None,
               return_shape: bool = False,
               abstracted_axes: Optional[Any] = None,
               ) -> Callable[..., Union[core.ClosedJaxpr,
                                        Tuple[core.ClosedJaxpr, Any]]]:
  """Creates a function that produces its jaxpr given example args.

  Args:
    fun: The function whose ``jaxpr`` is to be computed. Its positional
      arguments and return value should be arrays, scalars, or standard Python
      containers (tuple/list/dict) thereof.
    static_argnums: See the :py:func:`jax.jit` docstring.
    axis_env: Optional, a sequence of pairs where the first element is an axis
      name and the second element is a positive integer representing the size of
      the mapped axis with that name. This parameter is useful when lowering
      functions that involve parallel communication collectives, and it
      specifies the axis name/size environment that would be set up by
      applications of :py:func:`jax.pmap`.
    return_shape: Optional boolean, defaults to ``False``. If ``True``, the
      wrapped function returns a pair where the first element is the XLA
      computation and the second element is a pytree with the same structure as
      the output of ``fun`` and where the leaves are objects with ``shape``,
      ``dtype``, and ``named_shape`` attributes representing the corresponding
      types of the output leaves.

  Returns:
    A wrapped version of ``fun`` that when applied to example arguments returns
    a ``ClosedJaxpr`` representation of ``fun`` on those arguments. If the
    argument ``return_shape`` is ``True``, then the returned function instead
    returns a pair where the first element is the ``ClosedJaxpr``
    representation of ``fun`` and the second element is a pytree representing
    the structure, shape, dtypes, and named shapes of the output of ``fun``.

  A ``jaxpr`` is JAX's intermediate representation for program traces. The
  ``jaxpr`` language is based on the simply-typed first-order lambda calculus
  with let-bindings. :py:func:`make_jaxpr` adapts a function to return its
  ``jaxpr``, which we can inspect to understand what JAX is doing internally.
  The ``jaxpr`` returned is a trace of ``fun`` abstracted to
  :py:class:`ShapedArray` level. Other levels of abstraction exist internally.

  We do not describe the semantics of the ``jaxpr`` language in detail here, but
  instead give a few examples.

  >>> import jax
  >>>
  >>> def f(x): return jax.numpy.sin(jax.numpy.cos(x))
  >>> print(f(3.0))
  -0.83602
  >>> jax.make_jaxpr(f)(3.0)
  { lambda ; a:f32[]. let b:f32[] = cos a; c:f32[] = sin b in (c,) }
  >>> jax.make_jaxpr(jax.grad(f))(3.0)
  { lambda ; a:f32[]. let
      b:f32[] = cos a
      c:f32[] = sin a
      _:f32[] = sin b
      d:f32[] = cos b
      e:f32[] = mul 1.0 d
      f:f32[] = neg e
      g:f32[] = mul f c
    in (g,) }
  """
  check_callable(fun)
  static_argnums = _ensure_index_tuple(static_argnums)

  def abstractify(args, kwargs):
    flat_args, in_tree = tree_flatten((args, kwargs))
    if abstracted_axes is None:
      return map(shaped_abstractify, flat_args), in_tree, [True] * len(flat_args)
    else:
      axes_specs = _flat_axes_specs(abstracted_axes, *args, **kwargs)
      in_type = pe.infer_lambda_input_type(axes_specs, flat_args)
      in_avals, keep_inputs = unzip2(in_type)
      return in_avals, in_tree, keep_inputs

  @wraps(fun)
  @api_boundary
  def make_jaxpr_f(*args, **kwargs):
    f = lu.wrap_init(fun)
    if static_argnums:
      dyn_argnums = [i for i in range(len(args)) if i not in static_argnums]
      f, args = argnums_partial(f, dyn_argnums, args)
    in_avals, in_tree, keep_inputs = abstractify(args, kwargs)
    in_type = tuple(zip(in_avals, keep_inputs))
    f, out_tree = flatten_fun(f, in_tree)
    f = lu.annotate(f, in_type)
    debug_info = pe.debug_info(fun, in_tree, out_tree, True, 'make_jaxpr')
    with ExitStack() as stack:
      for axis_name, size in axis_env or []:
        stack.enter_context(core.extend_axis_env(axis_name, size, None))
      jaxpr, out_type, consts = pe.trace_to_jaxpr_dynamic2(
          f, debug_info=debug_info)
    closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
    if return_shape:
      out_avals, _ = unzip2(out_type)
      out_shapes_flat = [
          ShapeDtypeStruct(a.shape, a.dtype, a.named_shape) for a in out_avals]
      return closed_jaxpr, tree_unflatten(out_tree(), out_shapes_flat)
    return closed_jaxpr

  make_jaxpr_f.__name__ = f"make_jaxpr({make_jaxpr.__name__})"
  return make_jaxpr_f
