def _prepare_axis_resources(axis_resources,
                            arg_name,
                            allow_unconstrained_dims=False):
  # PyTrees don't treat None values as leaves, so we use an is_leaf function.
  entries, treedef = tree_flatten(axis_resources, is_leaf=lambda x: x is None)
  what = f"{arg_name} leaf specifications"
  # All entries should be specified or if unspecified then there should only
  # be 1 entry for that since _UNSPECIFIED is a private API.
  _check_all_or_none_unspecified(entries, arg_name)

  new_entries = []
  for entry in entries:
    if _is_unspecified_or_from_gda_or_auto(entry):
      new_entries.append(entry)
    elif isinstance(entry, Sharding):
      if isinstance(entry, PmapSharding):
        raise ValueError(f'One of {what} got sharding {entry} which is not '
                         'allowed.')
      if not isinstance(entry, XLACompatibleSharding):
        raise ValueError(f'One of {what} got sharding {entry} which is not a '
                         'subclass of XLACompatibleSharding.')
      new_entries.append(entry)
    else:
      new_entries.append(ParsedPartitionSpec.from_user_input(
          entry, what, allow_unconstrained_dims=allow_unconstrained_dims))

  _check_unique_resources(new_entries, arg_name)
  return tree_unflatten(treedef, new_entries), new_entries, treedef
