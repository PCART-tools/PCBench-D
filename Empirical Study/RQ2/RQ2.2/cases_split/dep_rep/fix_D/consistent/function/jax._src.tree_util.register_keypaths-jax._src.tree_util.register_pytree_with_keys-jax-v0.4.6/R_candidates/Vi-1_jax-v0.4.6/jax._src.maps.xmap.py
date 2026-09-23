def xmap(fun: Callable,
         in_axes,
         out_axes,
         *,
         axis_sizes: Dict[AxisName, int] = {},
         axis_resources: Dict[AxisName, ResourceSet] = {},
         donate_argnums: Union[int, Sequence[int]] = (),
         backend: Optional[str] = None) -> stages.Wrapped:
  """Assign a positional signature to a program that uses named array axes.

  .. warning::
    This is an experimental feature and the details can change at
    any time. Use at your own risk!

  .. warning::
    This docstring is aspirational. Not all features of the named axis
    programming model have been implemented just yet.

  The usual programming model of JAX (or really NumPy) associates each array
  with two pieces of metadata describing its type: the element type (``dtype``)
  and the ``shape``. :py:func:`xmap` extends this model by adding support for
  *named axes*.  In particular, each array used in a function wrapped by
  :py:func:`xmap` can additionally have a non-empty ``named_shape`` attribute,
  which can be used to query the set of named axes (introduced by
  :py:func:`xmap`) appearing in that value along with their shapes.
  Furthermore, in most places where positional axis indices are allowed (for
  example the `axes` arguments in :py:func:`sum`), bound axis names are also
  accepted. The :py:func:`einsum` language is extended inside :py:func:`xmap`
  to additionally allow contractions that involve named axes.  Broadcasting of
  named axes happens *by name*, i.e. all axes with equal names are expected to
  have equal shapes in all arguments of a broadcasting operation, while the
  result has a (set) union of all named axes.  The positional semantics of the
  program remain unchanged, and broadcasting still implicitly right-aligns
  positional axes for unification. For an extended description of the
  :py:func:`xmap` programming model, please refer to the :py:func:`xmap`
  tutorial notebook in main JAX documentation.

  Note that since all top-level JAX expressions are interpreted in the NumPy
  programming model, :py:func:`xmap` can also be seen as an adapter that
  converts a function that uses named axes (including in arguments and returned
  values) into one that takes and returns values that only have positional
  axes.

  The default lowering strategy of :py:func:`xmap` converts all named axes into
  positional axes, working similarly to multiple applications of
  :py:func:`vmap`. However, this behavior can be further customized by the
  ``axis_resources`` argument.  When specified, each axis introduced by
  :py:func:`xmap` can be assigned to one or more *resource axes*. Those include
  the axes of the hardware mesh, as defined by the :py:class:`Mesh` context
  manager. Each value that has a named axis in its ``named_shape`` will be
  partitioned over all mesh axes that axis is assigned to. Hence,
  :py:func:`xmap` can be seen as an alternative to :py:func:`pmap` that also
  exposes a way to automatically partition the computation over multiple
  devices.

  .. warning::
    While it is possible to assign multiple axis names to a single resource axis,
    care has to be taken to ensure that none of those named axes co-occur in a
    ``named_shape`` of any value in the named program. At the moment this is
    **completely unchecked** and will result in **undefined behavior**. The
    final release of :py:func:`xmap` will enforce this invariant, but it is a
    work in progress.

    Note that you do not have to worry about any of this for as long as no
    resource axis is repeated in ``axis_resources.values()``.

  Note that any assignment of ``axis_resources`` doesn't ever change the
  results of the computation, but only how it is carried out (e.g. how many
  devices are used).  This makes it easy to try out various ways of
  partitioning a single program in many distributed scenarios (both small- and
  large-scale), to maximize the performance.  As such, :py:func:`xmap` can be
  seen as a way to seamlessly interpolate between :py:func:`vmap` and
  :py:func:`pmap`-style execution.

  Args:
    fun: Function that uses named axes. Its arguments and return
      value should be arrays, scalars, or (nested) standard Python containers
      (tuple/list/dict) thereof (in general: valid pytrees).
    in_axes: A Python object with the same container (pytree) structure as the
      signature of arguments to ``fun``, but with a positional-to-named axis
      mapping in place of every array argument. The valid positional-to-named
      mappings are: (1) a ``Dict[int, AxisName]`` specifying that a positional
      dimensions given by dictionary keys are to be converted to named axes
      of given names (2) a list of axis names that ends with the Ellipsis object
      (``...``) in which case a number of leading positional axes of the argument
      will be converted into named axes inside the function. Note that ``in_axes``
      can also be a prefix of the argument container structure, in which case the
      mapping is repeated for all arrays in the collapsed subtree.
    out_axes: A Python object with the same container (pytree) structure as the
      returns of ``fun``, but with a positional-to-named axis mapping in place
      of every returned array. The valid positional-to-named mappings are the same
      as in ``in_axes``. Note that ``out_axes`` can also be a prefix of the return
      container structure, in which case the mapping is repeated for all arrays
      in the collapsed subtree.
    axis_sizes: A dict mapping axis names to their sizes. All axes defined by xmap
      have to appear either in ``in_axes`` or ``axis_sizes``. Sizes of axes
      that appear in ``in_axes`` are inferred from arguments whenever possible.
      In multi-host scenarios, the user-specified sizes are expected to be the
      global axis sizes (and might not match the expected size of local inputs).
    axis_resources: A dictionary mapping the axes introduced in this
      :py:func:`xmap` to one or more resource axes. Any array that has in its
      shape an axis with some resources assigned will be partitioned over the
      resources associated with the respective resource axes.
    donate_argnums: Specify which argument buffers are "donated" to the computation.
      It is safe to donate argument buffers if you no longer need them once the
      computation has finished. In some cases XLA can make use of donated
      buffers to reduce the amount of memory needed to perform a computation,
      for example recycling one of your input buffers to store a result. You
      should not reuse buffers that you donate to a computation, JAX will raise
      an error if you try to.

      For more details on buffer donation see the `FAQ <https://jax.readthedocs.io/en/latest/faq.html#buffer-donation>`_.

    backend: This is an experimental feature and the API is likely to change.
      Optional, a string representing the XLA backend. 'cpu', 'gpu', or 'tpu'.

  Returns:
    A version of ``fun`` that takes in arrays with positional axes in place of
    named axes bound in this :py:func:`xmap` call, and results with all named
    axes converted to positional axes. If ``axis_resources`` is specified,
    ``fun`` can additionally execute in parallel on multiple devices.

  For example, :py:func:`xmap` makes it very easy to convert a function that
  computes the vector inner product (such as :py:func:`jax.numpy.vdot`) into
  one that computes a matrix multiplication:

  >>> import jax.numpy as jnp
  >>> x = jnp.arange(10).reshape((2, 5))
  >>> xmap(jnp.vdot,
  ...      in_axes=({0: 'left'}, {1: 'right'}),
  ...      out_axes=['left', 'right', ...])(x, x.T)
  Array([[ 30,  80],
         [ 80, 255]], dtype=int32)

  Note that the contraction in the program is performed over the positional axes,
  while named axes are just a convenient way to achieve batching. While this
  might seem like a silly example at first, it might turn out to be useful in
  practice, since with conjunction with ``axis_resources`` this makes it possible
  to implement a distributed matrix-multiplication in just a few lines of code::

    devices = np.array(jax.devices())[:4].reshape((2, 2))
    with Mesh(devices, ('x', 'y')):  # declare a 2D mesh with axes 'x' and 'y'
      distributed_out = xmap(
        jnp.vdot,
        in_axes=({0: 'left'}, {1: 'right'}),
        out_axes=['left', 'right', ...],
        axis_resources={'left': 'x', 'right': 'y'})(x, x.T)

  Still, the above examples are quite simple. After all, the xmapped
  computation was a simple NumPy function that didn't use the axis names at all!
  So, let's explore a slightly larger example which is linear regression::

    def regression_loss(x, y, w, b):
      # Contract over in_features. Batch and out_features are present in
      # both inputs and output, so they don't need to be mentioned
      y_pred = jnp.einsum('{in_features},{in_features}->{}', x, w) + b
      error = jnp.sum((y - y_pred) ** 2, axis='out_features')
      return jnp.mean(error, axis='batch')

    xmap(regression_loss,
         in_axes=(['batch', 'in_features', ...],
                  ['batch', 'out_features', ...],
                  ['in_features', 'out_features', ...],
                  ['out_features', ...]),
         out_axes={})  # Loss is reduced over all axes, including batch!

  .. note::
    When using ``axis_resources`` along with a mesh that is controlled by
    multiple JAX hosts, keep in mind that in any given process :py:func:`xmap`
    only expects the data slice that corresponds to its local devices to be
    specified. This is in line with the current multi-host :py:func:`pmap`
    programming model.
  """
  check_callable(fun)

  if isinstance(in_axes, list) and not _is_axes_leaf(in_axes):
    # To be a tree prefix of the positional args tuple, in_axes can never be a
    # list: if in_axes is not a leaf, it must be a tuple of trees. However,
    # in cases like these users expect tuples and lists to be treated
    # essentially interchangeably, so we canonicalize lists to tuples here
    # rather than raising an error. https://github.com/google/jax/issues/2367
    in_axes = tuple(in_axes)

  if in_axes == ():  # Allow empty argument lists
    in_axes, in_axes_entries = (), []
  else:
    in_axes, in_axes_entries, _ = _prepare_axes(in_axes, "in_axes")
  if out_axes == ():
    raise ValueError("xmapped functions cannot have no return values")
  else:
    out_axes, out_axes_entries, out_axes_treedef = _prepare_axes(out_axes, "out_axes")
    out_axes_entries = tuple(out_axes_entries)  # Make entries hashable

  axis_sizes_names = set(axis_sizes.keys())
  in_axes_names = set(it.chain(*(spec.keys() for spec in in_axes_entries)))
  defined_names = axis_sizes_names | in_axes_names
  out_axes_names = set(it.chain(*(spec.keys() for spec in out_axes_entries)))

  anon_serial_loops = []
  def normalize_resource(r) -> ResourceAxisName:
    if isinstance(r, SerialLoop):
      name = fresh_resource_name()
      anon_serial_loops.append((name, r.length))
      return name
    return r

  axes_with_resources = set(axis_resources.keys())
  if axes_with_resources - defined_names:
    raise ValueError(f"All axes that were assigned resources have to appear in "
                     f"in_axes or axis_sizes, but the following are missing: "
                     f"{axes_with_resources - defined_names}")
  if out_axes_names - defined_names:
    raise ValueError(f"All axis names appearing in out_axes must also appear in "
                     f"in_axes or axis_sizes, but the following are missing: "
                     f"{out_axes_names - defined_names}")

  normalized_axis_resources: Dict[AxisName, Tuple[ResourceAxisName, ...]] = {}
  for axis in defined_names:
    resources = axis_resources.get(axis, ())
    if not isinstance(resources, tuple):
      resources = (resources,)
    normalized_axis_resources[axis] = tuple(unsafe_map(normalize_resource, resources))
  frozen_axis_resources = FrozenDict(normalized_axis_resources)
  necessary_resources = set(it.chain(*frozen_axis_resources.values()))

  for axis, resources in frozen_axis_resources.items():
    if len(set(resources)) != len(resources):  # type: ignore
      raise ValueError(f"Resource assignment of a single axis must be a tuple of "
                       f"distinct resources, but specified {resources} for axis {axis}")

  donate_argnums = _ensure_index_tuple(donate_argnums)

  # A little performance optimization to avoid iterating over all args unnecessarily
  has_input_rank_assertions = any(spec.expected_rank is not None for spec in in_axes_entries)
  has_output_rank_assertions = any(spec.expected_rank is not None for spec in out_axes_entries)

  def infer_params(*args):
    # Putting this outside of fun_mapped would make resources lexically scoped
    resource_env = thread_resources.env
    available_resources = set(resource_env.shape.keys())

    if necessary_resources - available_resources:
      raise ValueError(f"In-scope resources are insufficient to execute the "
                       f"xmapped function. The missing resources are: "
                       f"{necessary_resources - available_resources}")

    args_flat, in_tree = tree_flatten(args)
    fun_flat, out_tree = flatten_fun_nokwargs(lu.wrap_init(fun), in_tree)
    if donate_argnums:
      donated_invars = donation_vector(donate_argnums, args, ())
    else:
      donated_invars = (False,) * len(args_flat)
    in_axes_flat = _flatten_axes("xmap in_axes", in_tree, in_axes, tupled_args=True)

    # Some pytree containers might be unhashable, so we flatten the out_axes
    # pytree into a treedef and entries which are guaranteed to be hashable.
    out_axes_thunk = HashableFunction(
      lambda: tuple(_flatten_axes("xmap out_axes", out_tree(), out_axes, tupled_args=False)),
      closure=(out_axes_entries, out_axes_treedef))

    if config.jax_array:
      in_positional_semantics = (_PositionalSemantics.GLOBAL,) * len(args_flat)
    else:
      in_positional_semantics = tuple(
          _PositionalSemantics.GLOBAL
          if isinstance(a, GlobalDeviceArray) else _positional_semantics.val
          for a in args_flat)
    out_positional_semantics = (
        _PositionalSemantics.GLOBAL
        if config.jax_array or config.jax_parallel_functions_output_gda
        else _positional_semantics.val)

    axis_resource_count = _get_axis_resource_count(
        frozen_axis_resources, resource_env, in_positional_semantics)

    for axis, size in axis_sizes.items():
      resources = axis_resource_count[axis]
      if size % resources.nglobal != 0:
        global_size = "Global size" if resources.distributed else "Size"
        raise ValueError(f"{global_size} of axis {axis} ({size}) is not divisible "
                         f"by the total number of resources assigned to this axis "
                         f"({frozen_axis_resources[axis]}, {resources.nglobal} in total)")
    frozen_global_axis_sizes = _get_axis_sizes(
        args_flat, in_axes_flat, axis_sizes, axis_resource_count,
        in_positional_semantics)

    missing_sizes = defined_names - set(frozen_global_axis_sizes.keys())
    if missing_sizes:
      raise ValueError(f"Failed to infer size of axes: {', '.join(unsafe_map(str, missing_sizes))}. "
                       f"You've probably passed in empty containers in place of arguments that had "
                       f"those axes in their in_axes. Provide the sizes of missing axes explicitly "
                       f"via axis_sizes to fix this error.")

    if has_input_rank_assertions:
      for arg, spec in zip(args_flat, in_axes_flat):
        if spec.expected_rank is not None and spec.expected_rank != arg.ndim:
          raise ValueError(f"xmap argument has an in_axes specification of {spec.user_repr}, "
                           f"which asserts that it should be of rank {spec.expected_rank}, "
                           f"but the argument has rank {arg.ndim} (and shape {arg.shape})")

    _check_gda_or_array_xmap_partitioning(frozen_axis_resources, resource_env,
                                 frozen_global_axis_sizes, in_axes_flat,
                                 in_positional_semantics, args_flat)

    params = dict(
      name=getattr(fun, '__name__', '<unnamed function>'),
      in_axes=tuple(in_axes_flat),
      out_axes_thunk=out_axes_thunk,
      donated_invars=donated_invars,
      global_axis_sizes=frozen_global_axis_sizes,
      axis_resources=frozen_axis_resources,
      resource_env=resource_env,
      backend=backend,
      spmd_in_axes=None,
      spmd_out_axes_thunk=None,
      in_positional_semantics=in_positional_semantics,
      out_positional_semantics=out_positional_semantics)
    return fun_flat, args_flat, params, in_tree, out_tree

  def verify_outputs(out_flat, out_tree, params):
    if has_output_rank_assertions:
      for out, spec in zip(out_flat, params['out_axes_thunk']()):
        if spec.expected_rank is not None and spec.expected_rank != out.ndim:
          raise ValueError(f"xmap output has an out_axes specification of {spec.user_repr}, "
                           f"which asserts that it should be of rank {spec.expected_rank}, "
                           f"but the output has rank {out.ndim} (and shape {out.shape})")
    return tree_unflatten(out_tree(), out_flat)

  def decorate_serial(f):
    for loop_params in reversed(anon_serial_loops):
      f = serial_loop(*loop_params)(f)
    return f

  @wraps(fun)
  @decorate_serial
  def fun_mapped(*args):
    tree_map(dispatch.check_arg, args)
    fun_flat, args_flat, params, _, out_tree = infer_params(*args)
    out_flat = xmap_p.bind(fun_flat, *args_flat, **params)
    return verify_outputs(out_flat, out_tree, params)

  @decorate_serial
  def lower(*args, _experimental_lowering_platform: Optional[str] = None):
    fun_flat, args_flat, params, in_tree, out_tree = infer_params(*args)
    avals_flat = [shaped_abstractify(arg) for arg in args_flat]
    computation = make_xmap_callable(
        fun_flat, params['name'], params['in_axes'], params['out_axes_thunk'],
        params['donated_invars'], params['global_axis_sizes'], params['axis_resources'],
        params['resource_env'], params['backend'], params['spmd_in_axes'],
        params['spmd_out_axes_thunk'], params['in_positional_semantics'],
        params['out_positional_semantics'],
        _experimental_lowering_platform, *avals_flat)

    in_tree = treedef_tuple([in_tree, tree_flatten({})[1]])
    in_avals = in_tree.unflatten(avals_flat)
    return stages.Lowered.from_flat_info(
        computation, in_tree, in_avals, donate_argnums, out_tree(),  # type: ignore
        no_kwargs=True)

  fun_mapped.lower = lower
  return fun_mapped
