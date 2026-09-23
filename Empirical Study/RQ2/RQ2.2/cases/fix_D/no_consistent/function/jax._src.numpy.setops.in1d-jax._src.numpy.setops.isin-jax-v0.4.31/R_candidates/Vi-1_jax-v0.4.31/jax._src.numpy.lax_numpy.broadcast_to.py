@util.implements(np.broadcast_to, lax_description="""\
The JAX version does not necessarily return a view of the input.
""")
def broadcast_to(array: ArrayLike, shape: DimSize | Shape) -> Array:
  return util._broadcast_to(array, shape)
