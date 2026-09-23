@util._wraps(np.broadcast_arrays, lax_description="""\
The JAX version does not necessarily return a view of the input.
""")
def broadcast_arrays(*args: ArrayLike) -> List[Array]:
  return util._broadcast_arrays(*args)
