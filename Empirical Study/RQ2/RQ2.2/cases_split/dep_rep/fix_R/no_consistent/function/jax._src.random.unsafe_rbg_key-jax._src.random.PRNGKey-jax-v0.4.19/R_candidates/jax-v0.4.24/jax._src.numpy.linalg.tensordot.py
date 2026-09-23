@implements(getattr(np.linalg, "tensordot", None))
def tensordot(x1: ArrayLike, x2: ArrayLike, /, *,
              axes: int | tuple[Sequence[int], Sequence[int]] = 2) -> Array:
  check_arraylike('jnp.linalg.tensordot', x1, x2)
  return jnp.tensordot(x1, x2, axes=axes)
