def semaphore_wait(sem_or_view, dec: int | jax.Array = 1):
  ref, indexers = _get_ref_and_indexers(sem_or_view)
  dec = jnp.asarray(dec, dtype=jnp.int32)
  args = [ref, indexers, dec]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_wait_p.bind(*flat_args, args_tree=args_tree)
