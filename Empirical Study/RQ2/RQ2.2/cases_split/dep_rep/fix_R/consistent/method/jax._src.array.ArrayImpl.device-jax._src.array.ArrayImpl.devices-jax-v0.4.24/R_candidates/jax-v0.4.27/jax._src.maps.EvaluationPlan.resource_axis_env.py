  @property
  def resource_axis_env(self):
    env = dict(self.resource_env.shape)
    for axis, size in self.axis_vmap_size.items():
      if size is None:
        continue
      vmap_axis = self.axis_subst_dict[axis][-1]
      env[vmap_axis] = size
    return env
