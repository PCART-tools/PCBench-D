@util.implements(getattr(np, "broadcast_shapes", None))
def broadcast_shapes(*shapes):
  if not shapes:
    return ()
  shapes = [(shape,) if np.ndim(shape) == 0 else tuple(shape) for shape in shapes]
  return lax.broadcast_shapes(*shapes)
