class EvaluationPlan(NamedTuple):
  """Encapsulates preprocessing common to top-level xmap invocations and its translation rule."""
  resource_env: ResourceEnv
  physical_axis_resources: dict[AxisName, tuple[ResourceAxisName, ...]]
  loop_axis_resources: dict[AxisName, tuple[ResourceAxisName, ...]]
  axis_subst_dict: dict[AxisName, tuple[ResourceAxisName, ...]]
  axis_vmap_size: dict[AxisName, int | None]

  @property
  def axis_subst(self) -> core.AxisSubst:
    return lambda name: self.axis_subst_dict.get(name, (name,))

  @property
  def resource_axis_env(self):
    env = dict(self.resource_env.shape)
    for axis, size in self.axis_vmap_size.items():
      if size is None:
        continue
      vmap_axis = self.axis_subst_dict[axis][-1]
      env[vmap_axis] = size
    return env

  @classmethod
  def from_axis_resources(cls,
                          axis_resources: dict[AxisName, tuple[ResourceAxisName, ...]],
                          resource_env: ResourceEnv,
                          global_axis_sizes: dict[AxisName, int]):
    physical_axis_resources, loop_axis_resources = _unzip_axis_resources(
            axis_resources, resource_env)
    axis_resource_count = _get_axis_resource_count(
        axis_resources, resource_env)
    axis_subst_dict = dict(axis_resources)
    axis_vmap_size: dict[AxisName, int | None] = {}
    for naxis, raxes in sorted(axis_resources.items(), key=lambda x: str(x[0])):
      num_resources = axis_resource_count[naxis]
      assert global_axis_sizes[naxis] % num_resources.nglobal == 0
      local_tile_size = global_axis_sizes[naxis] // num_resources.nglobal
      # We have to vmap when there are no resources (to handle the axis name!) or
      # when every resource gets chunks of values.
      if not raxes or local_tile_size > 1:
        axis_vmap_size[naxis] = local_tile_size
        axis_subst_dict[naxis] += (fresh_resource_name(naxis),)
      else:
        axis_vmap_size[naxis] = None
    return cls(resource_env,
               physical_axis_resources, loop_axis_resources,
               axis_subst_dict, axis_vmap_size)

  def subst_axes_with_resources(self, jaxpr):
    try:
      if any(self.loop_axis_resources.values()):
        _check_no_loop_collectives(jaxpr, self.loop_axis_resources)
      with core.extend_axis_env_nd(self.resource_axis_env.items()):
        return core.subst_axis_names_jaxpr(jaxpr, self.axis_subst)
    except core.DuplicateAxisNameError:
      raise AssertionError("Incomplete resource type-checking? Please open a bug report!")

  def vectorize_and_loop(self, f: lu.WrappedFun, in_axes, out_axes) -> lu.WrappedFun:
    vmap_axes = {
        naxis: raxes[-1]
        for naxis, raxes in self.axis_subst_dict.items()
        if self.axis_vmap_size[naxis] is not None
    }
    for naxis, vaxis in sorted(vmap_axes.items(), key=lambda x: x[1].uid):
      local_tile_size = self.axis_vmap_size[naxis]
      map_in_axes = tuple(unsafe_map(lambda spec: spec.get(naxis, None), in_axes))
      map_out_axes = tuple(unsafe_map(lambda spec: spec.get(naxis, None), out_axes))
      f = batching.vtile(f, map_in_axes, map_out_axes, tile_size=local_tile_size, axis_name=vaxis)

    used_loops = set(it.chain.from_iterable(self.loop_axis_resources.values()))
    if not used_loops:
      return f

    if len(used_loops) > 1:
      # TODO: Support multiple loops
      raise NotImplementedError("Only one loop per xmap is supported")
    loop_in_axes = _to_resource_axes(in_axes, self.loop_axis_resources)
    loop_out_axes = _to_resource_axes(out_axes, self.loop_axis_resources)
    loop_name, = used_loops
    loop_length = self.resource_env.shape[loop_name]
    def looped_f(*args):
      def body(i, _):
        # XXX: This call_wrapped is only valid under the assumption that scan
        #      only ever traces the body once (which it does at the moment).
        result = f.call_wrapped(
            *(_slice_tile(arg, spec.get(loop_name, None), i, loop_length)
              for arg, spec in zip(args, loop_in_axes)))
        return i + 1, result
      _, stacked_results = lax.scan(body, 0, (), length=loop_length)
      return [_merge_leading_axis(sresult, spec.get(loop_name, None))
              for sresult, spec in zip(stacked_results, loop_out_axes)]
    return lu.wrap_init(looped_f)

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
