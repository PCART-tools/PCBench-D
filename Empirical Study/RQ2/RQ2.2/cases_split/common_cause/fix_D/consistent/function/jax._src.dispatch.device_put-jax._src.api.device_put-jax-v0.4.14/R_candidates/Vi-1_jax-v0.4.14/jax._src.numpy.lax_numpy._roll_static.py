@partial(jit, static_argnums=(1, 2))
def _roll_static(a: Array, shift: Sequence[int], axis: Sequence[int]) -> Array:
  for ax, s in zip(*np.broadcast_arrays(axis, shift)):
    if a.shape[ax] == 0:
      continue
    i = (-s) % a.shape[ax]
    a = lax.concatenate([lax.slice_in_dim(a, i, a.shape[ax], axis=ax),
                         lax.slice_in_dim(a, 0, i, axis=ax)],
                        dimension=ax)
  return a
