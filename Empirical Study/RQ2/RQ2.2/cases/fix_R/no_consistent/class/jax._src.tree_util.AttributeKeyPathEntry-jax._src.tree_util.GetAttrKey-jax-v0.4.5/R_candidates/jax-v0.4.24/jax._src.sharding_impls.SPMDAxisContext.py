@dataclasses.dataclass(frozen=True)
class SPMDAxisContext:
  """A hardware axis context for parallel computations that use the GSPMD partitioner.

  This includes the mesh that will later by used to execute this computation,
  as well as a set of mesh axes that are currently (e.g. because the current lowering
  is invoked inside an xmap) lowered in the MANUAL sharding mode.
  """
  mesh: mesh_lib.Mesh
  manual_axes: frozenset[MeshAxisName] = frozenset()

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

  @property
  def unsafe_axis_env(self):
    return AxisEnv(
        nreps=self.mesh.size,
        names=self.mesh.axis_names,
        sizes=tuple(self.mesh.shape.values()))

  def extend_manual(self, axes: frozenset[MeshAxisName]) -> SPMDAxisContext:
    return SPMDAxisContext(self.mesh, self.manual_axes | axes)
