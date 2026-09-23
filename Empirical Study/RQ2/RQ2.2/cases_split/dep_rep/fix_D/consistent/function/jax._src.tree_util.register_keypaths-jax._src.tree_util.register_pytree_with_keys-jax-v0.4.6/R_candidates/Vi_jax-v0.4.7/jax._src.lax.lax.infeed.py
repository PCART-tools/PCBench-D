def infeed(token, shape=None, partitions=None):
  """Consumes an infeed value of `shape` from the host. Experimental.

  `token` is used to sequence infeed and outfeed effects.
  `partitions` may be specified inside a `sharded_jit` function.
  """
  flat_shapes, treedef = pytree.flatten(shape)
  for shape in flat_shapes:
    if not isinstance(shape, ShapedArray):
      raise TypeError("shape argument to infeed must be a pytree of "
                      "ShapedArray values, got {}".format(shape))
  if partitions is not None:
    # Always replicate token.
    # We specifically use type() to raise an error for PartitionSpecs.
    if type(partitions) != tuple:  # pylint: disable=unidiomatic-typecheck
      raise ValueError(f"'partitions' argument to infeed should be a tuple, "
                       f"got {partitions}")
    partitions = partitions + (None,)
  xs_and_token = infeed_p.bind(token, shapes=tuple(flat_shapes),
                               partitions=partitions)
  return (treedef.unflatten(xs_and_token[:-1]), xs_and_token[-1])
