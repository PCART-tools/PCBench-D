  def is_equivalent_to(self: XLACompatibleSharding,  # type: ignore
                       other: XLACompatibleSharding, ndim: int) -> bool:
    try:
      return (are_op_shardings_equal(self._to_xla_hlo_sharding(ndim),
                                      other._to_xla_hlo_sharding(ndim))
              and self._internal_device_list == other._internal_device_list and  # type: ignore
              self.memory_kind == other.memory_kind)
    # NotImplementedError is raised by PmapSharding because it can't lower
    # to OpSharding. So if `other` is a PmapSharding, default to a strict
    # equality check.
    except NotImplementedError:
      return self == other
