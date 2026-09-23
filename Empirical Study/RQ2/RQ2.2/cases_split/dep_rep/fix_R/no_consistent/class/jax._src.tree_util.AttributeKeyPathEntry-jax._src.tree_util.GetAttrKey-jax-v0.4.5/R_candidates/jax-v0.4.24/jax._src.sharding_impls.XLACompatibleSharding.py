@use_cpp_class(xc.XLACompatibleSharding)
class XLACompatibleSharding(sharding.Sharding):
  """A :class:`Sharding` that describes shardings expressible to XLA.

  Subclasses of :class:`XLACompatibleSharding` work with
  all JAX APIs and transformations that use XLA.
  """

  # Abstract methods below that subclasses should implement.

  @property
  def _device_assignment(self) -> XLADeviceAssignment:
    raise NotImplementedError('Subclasses should implement this method.')

  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    raise NotImplementedError('Subclasses should implement this method.')

  #############################################################################
  # Default implementations below that all subclasses will inherit.

  def devices_indices_map(self, global_shape: Shape) -> Mapping[Device, Index]:
    return common_devices_indices_map(self, global_shape)

  @functools.cached_property
  def _addressable_device_assignment(self) -> XLADeviceAssignment:
    if self.is_fully_addressable:
      return self._device_assignment
    if hasattr(self, '_internal_device_list'):
      return tuple(self._internal_device_list.addressable_device_list)
    return tuple(d for d in self._device_assignment
                 if d.process_index == d.client.process_index())

  def shard_shape(self, global_shape: Shape) -> Shape:
    return _common_shard_shape(self, global_shape)

  def is_equivalent_to(self: XLACompatibleSharding,  # type: ignore
                       other: XLACompatibleSharding, ndim: int) -> bool:
    try:
      return (are_op_shardings_equal(self._to_xla_hlo_sharding(ndim),
                                      other._to_xla_hlo_sharding(ndim))
              and self._device_assignment == other._device_assignment and
              self.memory_kind == other.memory_kind)
    # NotImplementedError is raised by PmapSharding because it can't lower
    # to OpSharding. So if `other` is a PmapSharding, default to a strict
    # equality check.
    except NotImplementedError:
      return self == other
