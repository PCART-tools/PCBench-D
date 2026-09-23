def pjit(
    fun: Callable,
    in_shardings=_UNSPECIFIED,
    out_shardings=_UNSPECIFIED,
    in_axis_resources=_UNSPECIFIED,
    out_axis_resources=_UNSPECIFIED,
    static_argnums: Union[int, Sequence[int], None] = None,
    static_argnames: Union[str, Iterable[str], None] = None,
    donate_argnums: Union[int, Sequence[int]] = (),
    keep_unused: bool = False,
    device: Optional[xc.Device] = None,
    backend: Optional[str] = None,
    inline: bool = False,
    abstracted_axes: Optional[Any] = None,
) -> stages.Wrapped:
  """Makes ``fun`` compiled and automatically partitioned across multiple devices.

  The returned function has semantics equivalent to those of ``fun``, but is
  compiled to an XLA computation that runs across multiple devices
  (e.g. multiple GPUs or multiple TPU cores). This can be useful if the jitted
  version of ``fun`` would not fit in a single device's memory, or to speed up
  ``fun`` by running each operation in parallel across multiple devices.

  The partitioning over devices happens automatically based on the
  propagation of the input partitioning specified in ``in_shardings`` and
  the output partitioning specified in ``out_shardings``. The resources
  specified in those two arguments must refer to mesh axes, as defined by
  the :py:func:`jax.sharding.Mesh` context manager. Note that the mesh
  definition at :func:`~pjit` application time is ignored, and the returned function
  will use the mesh definition available at each call site.

  Inputs to a :func:`~pjit`'d function will be automatically partitioned across devices
  if they're not already correctly partitioned based on ``in_shardings``.
  In some scenarios, ensuring that the inputs are already correctly pre-partitioned
  can increase performance. For example, if passing the output of one
  :func:`~pjit`'d function to another :func:`~pjit`’d function (or the same
  :func:`~pjit`’d function in a loop), make sure the relevant
  ``out_shardings`` match the corresponding ``in_shardings``.

  .. note::
    **Multi-process platforms:** On multi-process platforms such as TPU pods,
    :func:`~pjit` can be used to run computations across all available devices across
    processes. To achieve this, :func:`~pjit` is designed to be used in SPMD Python
    programs, where every process is running the same Python code such that all
    processes run the same :func:`~pjit`'d function in the same order.

    When running in this configuration, the mesh should contain devices across
    all processes. However, any input argument dimensions partitioned over
    multi-process mesh axes should be of size equal to the corresponding *local*
    mesh axis size, and outputs will be similarly sized according to the local
    mesh. ``fun`` will still be executed across *all* devices in the mesh,
    including those from other processes, and will be given a global view of the
    data spread across multiple processes as a single array. However, outside
    of :func:`~pjit` every process only "sees" its local piece of the input and output,
    corresponding to its local sub-mesh.

    This means that each process's participating local devices must form a
    _contiguous_ local sub-mesh within the full global mesh. A contiguous
    sub-mesh is one where all of its devices are adjacent within the global
    mesh, and form a rectangular prism.

    The SPMD model also requires that the same multi-process :func:`~pjit`'d
    functions must be run in the same order on all processes, but they can be
    interspersed with arbitrary operations running in a single process.

  Args:
    fun: Function to be compiled. Should be a pure function, as side-effects may
      only be executed once. Its arguments and return value should be arrays,
      scalars, or (nested) standard Python containers (tuple/list/dict) thereof.
      Positional arguments indicated by ``static_argnums`` can be anything at
      all, provided they are hashable and have an equality operation defined.
      Static arguments are included as part of a compilation cache key, which is
      why hash and equality operators must be defined.
    in_shardings: Pytree of structure matching that of arguments to ``fun``,
      with all actual arguments replaced by resource assignment specifications.
      It is also valid to specify a pytree prefix (e.g. one value in place of a
      whole subtree), in which case the leaves get broadcast to all values in
      that subtree.

      The valid resource assignment specifications are:
        - :py:obj:`None`, in which case the value will be replicated on all devices
        - :py:class:`XLACompatibleSharding`, which will decide how the value
          will be partitioned. With this, using a mesh context manager is not
          required.
        - :py:class:`PartitionSpec`, a tuple of length at most equal to the rank
          of the partitioned value. Each element can be a :py:obj:`None`, a mesh
          axis or a tuple of mesh axes, and specifies the set of resources assigned
          to partition the value's dimension matching its position in the spec.

      The size of every dimension has to be a multiple of the total number of
      resources assigned to it.
    out_shardings: Like ``in_shardings``, but specifies resource
      assignment for function outputs.
    in_axis_resources: (Deprecated) Please use in_shardings.
    out_axis_resources: (Deprecated) Please use out_shardings.
    static_argnums: An optional int or collection of ints that specify which
      positional arguments to treat as static (compile-time constant).
      Operations that only depend on static arguments will be constant-folded in
      Python (during tracing), and so the corresponding argument values can be
      any Python object.

      Static arguments should be hashable, meaning both ``__hash__`` and
      ``__eq__`` are implemented, and immutable. Calling the jitted function
      with different values for these constants will trigger recompilation.
      Arguments that are not arrays or containers thereof must be marked as
      static.

      If ``static_argnums`` is not provided, no arguments are treated as static.
    static_argnames: An optional string or collection of strings specifying
      which named arguments to treat as static (compile-time constant). See the
      comment on ``static_argnums`` for details. If not
      provided but ``static_argnums`` is set, the default is based on calling
      ``inspect.signature(fun)`` to find corresponding named arguments.
    donate_argnums: Specify which argument buffers are "donated" to the computation.
      It is safe to donate argument buffers if you no longer need them once the
      computation has finished. In some cases XLA can make use of donated
      buffers to reduce the amount of memory needed to perform a computation,
      for example recycling one of your input buffers to store a result. You
      should not reuse buffers that you donate to a computation, JAX will raise
      an error if you try to.
      For more details on buffer donation see the `FAQ <https://jax.readthedocs.io/en/latest/faq.html#buffer-donation>`_.
    keep_unused: If `False` (the default), arguments that JAX determines to be
      unused by `fun` *may* be dropped from resulting compiled XLA executables.
      Such arguments will not be transferred to the device nor provided to the
      underlying executable. If `True`, unused arguments will not be pruned.
    device: This argument is deprecated. Please put your arguments on the
      device you want before passing them to jit.
      Optional, the Device the jitted function will run on. (Available devices
      can be retrieved via :py:func:`jax.devices`.) The default is inherited
      from XLA's DeviceAssignment logic and is usually to use
      ``jax.devices()[0]``.
    backend: This argument is deprecated. Please put your arguments on the
      backend you want before passing them to jit.
      Optional, a string representing the XLA backend: ``'cpu'``, ``'gpu'``, or
      ``'tpu'``.
  Returns:
    A wrapped version of ``fun``, set up for just-in-time compilation and
    automatically partitioned by the mesh available at each call site.

  For example, a convolution operator can be automatically partitioned over
  an arbitrary set of devices by a single :func:`~pjit` application:

  >>> import jax
  >>> import jax.numpy as jnp
  >>> import numpy as np
  >>> from jax.sharding import Mesh, PartitionSpec
  >>> from jax.experimental.pjit import pjit
  >>>
  >>> x = jnp.arange(8, dtype=jnp.float32)
  >>> f = pjit(lambda x: jax.numpy.convolve(x, jnp.asarray([0.5, 1.0, 0.5]), 'same'),
  ...         in_shardings=None, out_shardings=PartitionSpec('devices'))
  >>> with Mesh(np.array(jax.devices()), ('devices',)):
  ...   print(f(x))  # doctest: +SKIP
  [ 0.5  2.   4.   6.   8.  10.  12.  10. ]
  """
  in_shardings, out_shardings = _resolve_axis_resources_and_shardings_arg(
      in_shardings, out_shardings, in_axis_resources, out_axis_resources)

  (in_shardings, out_shardings, donate_argnums, static_argnums,
   static_argnames) = pre_infer_params(
       fun, in_shardings, out_shardings, donate_argnums,
       static_argnums, static_argnames, device, backend, abstracted_axes)

  def infer_params(*args, **kwargs):
    # Putting this outside of wrapped would make resources lexically scoped
    resource_env = mesh.thread_resources.env
    pjit_info_args = PjitInfo(
          fun=fun, in_shardings=in_shardings,
          out_shardings=out_shardings, static_argnums=static_argnums,
          static_argnames=static_argnames, donate_argnums=donate_argnums,
          device=device, backend=backend, keep_unused=keep_unused,
          inline=inline, resource_env=resource_env,
          abstracted_axes=abstracted_axes)
    return common_infer_params(pjit_info_args, *args, **kwargs)

  has_explicit_sharding = _pjit_explicit_sharding(
      in_shardings, out_shardings, device, backend)
  return post_infer_params(fun, infer_params, static_argnums, static_argnames,
                           donate_argnums, abstracted_axes,
                           has_explicit_sharding)
