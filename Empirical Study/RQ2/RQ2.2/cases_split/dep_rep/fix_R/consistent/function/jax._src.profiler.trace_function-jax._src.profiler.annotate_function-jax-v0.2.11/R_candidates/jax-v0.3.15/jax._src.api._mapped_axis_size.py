def _mapped_axis_size(tree, vals, dims, name, *, kws=False):
  if not vals:
    args, kwargs = tree_unflatten(tree, vals)
    raise ValueError(
        f"{name} wrapped function must be passed at least one argument "
        f"containing an array, got empty *args={args} and **kwargs={kwargs}"
    )

  def _get_axis_size(name: str, shape: Tuple[core.AxisSize, ...], axis: int
                     ) -> core.AxisSize:
    try:
      return shape[axis]
    except (IndexError, TypeError) as e:
      min_rank = axis + 1 if axis >= 0 else -axis
      raise ValueError(
          f"{name} was requested to map its argument along axis {axis}, "
          f"which implies that its rank should be at least {min_rank}, "
          f"but is only {len(shape)} (its shape is {shape})") from e

  axis_sizes = core.dedup_referents(
      _get_axis_size(name, np.shape(x), d) for x, d in zip(vals, dims)
      if d is not None)
  if len(axis_sizes) == 1:
    return axis_sizes[0]
  if not axis_sizes:
    msg = f"{name} must have at least one non-None value in in_axes"
    raise ValueError(msg)
  msg = f"{name} got inconsistent sizes for array axes to be mapped:\n" + "{}"
  # we switch the error message based on whether args is a tuple of arrays,
  # in which case we can produce an error message based on argument indices,
  # or if it has nested containers.
  if kws:
    position_only_tree, leaf = treedef_children(tree)
    if not treedef_is_leaf(leaf):
      sizes = [x.shape[d] if d is not None else None for x, d in zip(vals, dims)]
      sizes = tree_unflatten(tree, sizes)
      raise ValueError(msg.format(f"the tree of axis sizes is:\n{sizes}")) from None
    # if keyword arguments are included in the tree, we adapt the error
    # message only to be about the positional arguments
    tree = position_only_tree

  # TODO(mattjj,phawkins): add a way to inspect pytree kind more directly
  if tree == tree_flatten((0,) * tree.num_leaves)[1]:
    lines1 = [f"arg {i} has shape {np.shape(x)} and axis {d} is to be mapped"
              for i, (x, d) in enumerate(zip(vals, dims))]
    sizes = collections.defaultdict(list)
    for i, (x, d) in enumerate(zip(vals, dims)):
      if d is not None:
        sizes[x.shape[d]].append(i)
    lines2 = ["{} {} {} {} to be mapped of size {}".format(
                "args" if len(idxs) > 1 else "arg",
                ", ".join(map(str, idxs)),
                "have" if len(idxs) > 1 else "has",
                "axes" if len(idxs) > 1 else "an axis",
                size)
              for size, idxs in sizes.items()]
    raise ValueError(msg.format("\n".join(lines1 + ["so"] + lines2))) from None
  else:
    sizes = [x.shape[d] if d is not None else None for x, d in zip(vals, dims)]
    sizes = tree_unflatten(tree, sizes)
    raise ValueError(msg.format(f"the tree of axis sizes is:\n{sizes}")) from None
