def outfeed(token, xs, partitions = None):
  """Outfeeds value `xs` to the host. Experimental.

  `token` is used to sequence infeed and outfeed effects.
  `partitions` may be specified inside a `sharded_jit` or `pjit` function.
  """
  if partitions is not None:
    # We specifically use type() to raise an error for PartitionSpecs.
    if type(partitions) != tuple:  # pylint: disable=unidiomatic-typecheck
      raise ValueError(f"'partitions' argument to outfeed should be a tuple, "
                       f"got {partitions}")
  flat_xs, _ = tree_util.tree_flatten(xs)
  return outfeed_p.bind(token, *flat_xs, partitions=partitions)
