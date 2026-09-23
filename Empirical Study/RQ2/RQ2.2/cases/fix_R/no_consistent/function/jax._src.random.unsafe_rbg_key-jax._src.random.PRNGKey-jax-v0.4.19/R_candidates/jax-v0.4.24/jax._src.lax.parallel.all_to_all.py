def all_to_all(x, axis_name, split_axis, concat_axis, *, axis_index_groups=None, tiled=False):
  """Materialize the mapped axis and map a different axis.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  In the output, the input mapped axis ``axis_name`` is materialized at the
  logical axis position ``concat_axis``, and the input unmapped axis at position
  ``split_axis`` is mapped with the name ``axis_name``.

  The group size of the mapped axis size must be equal to the size of the
  unmapped axis; that is, we must have
  ``lax.psum(1, axis_name, axis_index_groups=axis_index_groups) == x.shape[axis]``.
  By default, when ``axis_index_groups=None``, this encompasses all the devices.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    split_axis: int indicating the unmapped axis of ``x`` to map with the name
      ``axis_name``.
    concat_axis: int indicating the position in the output to materialize the
      mapped axis of the input with the name ``axis_name``.
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would run all_to_all over the first
      two and last two replicas). Groups must cover all axis indices exactly
      once, and all groups must be the same size.
    tiled: when True, all_to_all will divide split_axis into chunks and concatenate
      them along concat_axis. In particular, no dimensions are added or removed.
      False by default.

  Returns:
    When tiled is False, array(s) with shape given by the expression::

      np.insert(np.delete(x.shape, split_axis), concat_axis, axis_size)

    where ``axis_size`` is the size of the mapped axis named ``axis_name`` in
    the input ``x``, i.e. ``axis_size = lax.psum(1, axis_name)``.

    Otherwise array with shape similar to the input shape, except with split_axis
    divided by axis size and concat_axis multiplied by axis size.
  """
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  def bind(x, split_axis=split_axis, concat_axis=concat_axis):
    group_size = psum(1, axis_name, axis_index_groups=axis_index_groups)
    if tiled:
      if x.shape[split_axis] % group_size != 0:
        raise ValueError(f"The size of all_to_all split_axis ({x.shape[split_axis]}) "
                         f"has to be divisible by the size of the named axis "
                         f"{axis_name} ({group_size})")
    else:
      if group_size != x.shape[split_axis]:
        msg = ("all_to_all requires the size of the mapped axis axis_name to "
               "equal x.shape[split_axis], but they are {} and {} respectively.")
        raise ValueError(msg.format(group_size, x.shape[split_axis]))
      if split_axis < concat_axis:
        concat_axis += 1  # concat_axis gives a position _after_ split_axis is removed
        x = lax.expand_dims(x, (concat_axis,))  # insert the new axis
      elif split_axis == concat_axis:
        pass
      else:  # concat_axis < split_axis
        x = lax.expand_dims(x, (concat_axis,))  # insert the new axis
        split_axis += 1   # we have a new axis before split_axis now
    result = all_to_all_p.bind(x, split_axis=split_axis, concat_axis=concat_axis,
                               axis_name=axis_name,
                               axis_index_groups=axis_index_groups)
    if not tiled and split_axis != concat_axis:
      result = lax.squeeze(result, (split_axis,))
    return result

  return tree_util.tree_map(bind, x)
