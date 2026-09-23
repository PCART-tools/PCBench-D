  def subst_axes_with_resources(self, jaxpr):
    try:
      if any(self.loop_axis_resources.values()):
        _check_no_loop_collectives(jaxpr, self.loop_axis_resources)
      with core.extend_axis_env_nd(self.resource_axis_env.items()):
        return core.subst_axis_names_jaxpr(jaxpr, self.axis_subst)
    except core.DuplicateAxisNameError:
      raise AssertionError("Incomplete resource type-checking? Please open a bug report!")
