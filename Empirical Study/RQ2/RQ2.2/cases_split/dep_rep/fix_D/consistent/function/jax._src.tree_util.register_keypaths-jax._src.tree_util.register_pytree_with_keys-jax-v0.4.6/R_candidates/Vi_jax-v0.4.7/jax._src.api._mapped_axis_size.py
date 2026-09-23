def _mapped_axis_size(fn, tree, vals, dims, name):
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
      # TODO(mattjj): better error message here
      raise ValueError(
          f"{name} was requested to map its argument along axis {axis}, "
          f"which implies that its rank should be at least {min_rank}, "
          f"but is only {len(shape)} (its shape is {shape})") from e

  sizes = core.dedup_referents(_get_axis_size(name, np.shape(x), d)
                               for x, d in zip(vals, dims) if d is not None)
  if len(sizes) == 1:
    sz, = sizes
    return sz
  if not sizes:
    msg = f"{name} must have at least one non-None value in in_axes"
    raise ValueError(msg)

  msg = [f"{name} got inconsistent sizes for array axes to be mapped:\n"]
  args, kwargs = tree_unflatten(tree, vals)
  try:
    ba = inspect.signature(fn).bind(*args, **kwargs)
  except (TypeError, ValueError):
    ba = None
  if ba is None:
    args_paths = [f'args{keystr(p)} '
                  f'of type {shaped_abstractify(x).str_short()}'
                  for p, x in generate_key_paths(args)]
    kwargs_paths = [f'kwargs{keystr(p)} '
                    f'of type {shaped_abstractify(x).str_short()}'
                    for p, x in generate_key_paths(kwargs)]
    key_paths = [*args_paths, *kwargs_paths]
  else:
    key_paths = [f'argument {name}{keystr(p)} '
                 f'of type {shaped_abstractify(x).str_short()}'
                 for name, arg in ba.arguments.items()
                 for p, x in generate_key_paths(arg)]
  all_sizes = [_get_axis_size(name, np.shape(x), d) if d is not None else None
               for x, d in zip(vals, dims)]
  size_counts = collections.Counter(s for s in all_sizes if s is not None)
  (sz, ct), *other_counts = counts = size_counts.most_common()
  def _all_sizes_index(sz):
    for i, isz in enumerate(all_sizes):
      if core.symbolic_equal_dim(isz, sz): return i
    assert False, (sz, all_sizes)

  ex, *examples = [key_paths[_all_sizes_index(sz)] for sz, _ in counts]
  ax, *axs = [dims[_all_sizes_index(sz)] for sz, _ in counts]
  if ct == 1:
    msg.append(f"  * one axis had size {sz}: axis {ax} of {ex};\n")
  else:
    msg.append(f"  * most axes ({ct} of them) had size {sz}, e.g. axis {ax} of {ex};\n")
  for ex, ax, (sz, ct) in zip(examples, axs, other_counts):
    if ct == 1:
      msg.append(f"  * one axis had size {sz}: axis {ax} of {ex};\n")
    else:
      msg.append(f"  * some axes ({ct} of them) had size {sz}, e.g. axis {ax} of {ex};\n")
  raise ValueError(''.join(msg)[:-2])  # remove last semicolon and newline
