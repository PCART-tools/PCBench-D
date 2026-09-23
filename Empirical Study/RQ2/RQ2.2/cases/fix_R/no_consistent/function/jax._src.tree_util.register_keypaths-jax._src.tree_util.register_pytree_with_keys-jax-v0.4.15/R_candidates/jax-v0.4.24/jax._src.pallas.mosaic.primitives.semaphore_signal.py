def semaphore_signal(
    sem_or_view,
    inc: int | jax.Array = 1,
    *,
    device_id: int | jax.Array | None | tuple[int | jax.Array, ...] = None,
    device_id_type: DeviceIdType = DeviceIdType.MESH,
):
  ref, indexers = _get_ref_and_indexers(sem_or_view)
  inc = jnp.asarray(inc, dtype=jnp.int32)
  args = [ref, indexers, inc, device_id]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_signal_p.bind(
      *flat_args,
      args_tree=args_tree,
      device_id_type=device_id_type,
  )
