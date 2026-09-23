  @property
  def axis_env(self):
    # All collectives that touch axis_env should remember to set use_global_device_ids
    # when this context is enabled!
    if self.manual_axes != frozenset(self.mesh.axis_names):
      raise NotImplementedError(
          "Collectives in manually partitioned computations are only supported "
          "when all mesh axes are partitioned manually (no partial automatic sharding). "
          "Make sure that you mention all mesh axes in axis_resources!")
    return self.unsafe_axis_env
