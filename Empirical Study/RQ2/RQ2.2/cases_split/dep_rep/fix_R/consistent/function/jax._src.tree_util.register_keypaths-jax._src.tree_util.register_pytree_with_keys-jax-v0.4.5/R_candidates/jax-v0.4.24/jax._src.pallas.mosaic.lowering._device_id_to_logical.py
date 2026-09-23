def _device_id_to_logical(
    ctx: LoweringRuleContext, device_id,
    device_id_type: tpu_primitives.DeviceIdType):
  if device_id_type is tpu_primitives.DeviceIdType.MESH:
    # Mesh means we are passed the mesh coordinates for the device
    device_ids = tree_util.tree_leaves(device_id)
    mesh_strides = ctx.lowering_context.mesh_context.mesh_strides
    def _linearize_mesh_indices(*indices):
      return sum([a * b for a, b in zip(indices, mesh_strides)])
    lower_ctx = LoweringRuleContext(
        lowering_context=ctx.lowering_context,
        avals_in=[jax_core.ShapedArray((), jnp.int32)] * len(device_ids),
        avals_out=[jax_core.ShapedArray((), jnp.int32)],
        block_shapes=(None,) * len(device_ids),
    )
    return lower_fun(_linearize_mesh_indices, multiple_results=False)(
        lower_ctx, *device_ids)
  elif device_id_type is tpu_primitives.DeviceIdType.LOGICAL:
    return device_id
  raise NotImplementedError(f"Unsupported device id type: {device_id_type}")
