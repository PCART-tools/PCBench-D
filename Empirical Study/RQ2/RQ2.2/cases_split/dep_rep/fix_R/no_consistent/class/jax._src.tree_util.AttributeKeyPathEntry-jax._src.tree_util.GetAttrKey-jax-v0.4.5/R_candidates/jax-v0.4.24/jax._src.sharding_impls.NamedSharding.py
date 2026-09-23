@use_cpp_class(xc.NamedSharding)
class NamedSharding(XLACompatibleSharding):
  r"""A :class:`NamedSharding` expresses sharding using named axes.

  A :class:`NamedSharding` is a pair of a :class:`Mesh` of devices and
  :class:`PartitionSpec` which describes how to shard an array across that
  mesh.

  A :class:`Mesh` is a multidimensional NumPy array of JAX devices,
  where each axis of the mesh has a name, e.g. ``'x'`` or ``'y'``.

  A :class:`PartitionSpec` is a tuple, whose elements can be a ``None``,
  a mesh axis, or a tuple of mesh axes. Each element describes how an input
  dimension is partitioned across zero or more mesh dimensions. For example,
  ``PartitionSpec('x', 'y')`` says that the first dimension of data
  is sharded across ``x`` axis of the mesh, and the second dimension is sharded
  across ``y`` axis of the mesh.

  The Distributed arrays and automatic parallelization
  (https://jax.readthedocs.io/en/latest/notebooks/Distributed_arrays_and_automatic_parallelization.html#namedsharding-gives-a-way-to-express-shardings-with-names)
  tutorial has more details and diagrams that explain how
  :class:`Mesh` and :class:`PartitionSpec` are used.

  Args:
    mesh: A :class:`jax.sharding.Mesh` object.
    spec: A :class:`jax.sharding.PartitionSpec` object.

  Example:

    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> mesh = Mesh(np.array(jax.devices()).reshape(2, 4), ('x', 'y'))
    >>> spec = P('x', 'y')
    >>> named_sharding = jax.sharding.NamedSharding(mesh, spec)
  """

  mesh: mesh_lib.Mesh
  spec: PartitionSpec
  _memory_kind: str | None
  _parsed_pspec: ParsedPartitionSpec
  _manual_axes: frozenset[MeshAxisName]

  @use_cpp_method()
  def __init__(
      self, mesh: mesh_lib.Mesh, spec: PartitionSpec, *,
      memory_kind: str | None = None, _parsed_pspec=None,
      _manual_axes=frozenset()):
    self.mesh = mesh
    self.spec = spec
    self._memory_kind = memory_kind
    self._parsed_pspec = _parsed_pspec
    self._manual_axes = _manual_axes
    self._preprocess()

  def _preprocess(self):
    # This split exists because you can pass `_parsed_pspec` that has been
    # modified from the original. For example: Adding extra dimension to
    # axis_resources for vmap handlers. In such cases you need to preserve the
    # `sync` attribute of parsed pspecs.
    # PartitionSpec is inferred from the parsed pspec in this case.
    # TODO(yaskatariya): Remove this and replace this with a normalized
    # representation of Parsed Pspec
    if self._parsed_pspec is None:
      self._parsed_pspec, _, _ = prepare_axis_resources(
          PartitionSpec() if self.spec is None else self.spec,
          "NamedSharding spec", allow_unconstrained_dims=True)

    _check_mesh_resource_axis(self.mesh, self._parsed_pspec)

  def __repr__(self):
    mesh_repr = ", ".join(f"'{k}': {v}" for k, v in self.mesh.shape.items())
    mem = '' if self.memory_kind is None else f', memory_kind={self.memory_kind}'
    return f'NamedSharding(mesh=Mesh({mesh_repr}), spec={self.spec}{mem})'

  def __reduce__(self):
    return (type(self), (self.mesh, self.spec),
            {'memory_kind': self.memory_kind,
             '_manual_axes': self._manual_axes})

  @property
  def memory_kind(self) -> str | None:
    return self._memory_kind

  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash(
          (self.mesh, self.memory_kind, self._parsed_pspec, self._manual_axes))
    return self._hash

  def __eq__(self, other):
    if not isinstance(other, NamedSharding):
      return False
    if id(self) == id(other):
      return True
    if (self._parsed_pspec != other._parsed_pspec
        or self.memory_kind != other.memory_kind
        or self._manual_axes != other._manual_axes):
      return False
    return id(self.mesh) == id(other.mesh) or self.mesh == other.mesh

  def is_compatible_aval(self, aval_shape: Shape):
    assert self._parsed_pspec is not None
    if len(aval_shape) < len(self._parsed_pspec):
      extra_msg = (' For scalars the PartitionSpec should be P()'
                   if len(aval_shape) == 0 else '')
      raise ValueError(
          f"Sharding {self} is only valid for values of rank at least "
          f"{len(self._parsed_pspec)}, but was applied to a value of rank "
          f"{len(aval_shape)}.{extra_msg}")

  @classmethod
  def _from_parsed_pspec(
      cls, mesh, parsed_pspec, *, memory_kind=None, _manual_axes=frozenset()
  ):
    return cls(mesh, parsed_pspec.get_partition_spec(),
                memory_kind=memory_kind, _parsed_pspec=parsed_pspec,
                _manual_axes=_manual_axes)

  @property
  def device_set(self) -> set[Device]:
    return self.mesh._flat_devices_set

  @property
  def _device_assignment(self) -> XLADeviceAssignment:
    return self.mesh._flat_devices_tuple

  @property
  def is_fully_addressable(self) -> bool:
    # Speed up `is_fully_addressable` since there is a high chance that the
    # mesh across multiple NamedSharding objects will be the same.
    return not self.mesh.is_multi_process

  @property
  def addressable_devices(self) -> set[Device]:
    # Override addressable devices because there is a high chance that the mesh
    # across multiple NamedSharding objects will be the same.
    return self.mesh._local_devices_set

  @functools.cached_property
  def is_fully_replicated(self) -> bool:
    if self.mesh.size == 1:
      return True
    array_mapping = cast(ParsedPartitionSpec, get_array_mapping(self._parsed_pspec))
    mesh_shape = self.mesh.shape
    num_partitions = 1
    for name in array_mapping:
      num_partitions *= mesh_shape[name]
    return num_partitions == 1

  def with_memory_kind(self, kind: str) -> NamedSharding:
    return NamedSharding(self.mesh, self.spec, memory_kind=kind)

  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return named_sharding_to_xla_hlo_sharding(self, num_dimensions)
