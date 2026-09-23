  def to_mesh_axes(self, in_axes, out_axes=None):
    """
    Convert in/out_axes parameters ranging over logical dimensions to
    in/out_axes that range over the mesh dimensions.
    """
    if out_axes is None:
      return _to_resource_axes(in_axes, self.physical_axis_resources)
    else:
      return (_to_resource_axes(in_axes, self.physical_axis_resources),
              _to_resource_axes(out_axes, self.physical_axis_resources))
