def visualize_sharding(shape: Sequence[int], sharding: Sharding, *,
                       use_color: bool = True, scale: float = 1.,
                       min_width: int = 9, max_width: int = 80,
                       color_map: Optional[ColorMap] = None):
  """Visualizes a ``Sharding`` using ``rich``."""
  if not RICH_ENABLED:
    raise ValueError("`visualize_sharding` requires `rich` to be installed.")
  if len(shape) > 2 or len(shape) < 1:
    raise ValueError(
        "`visualize_sharding` only works for shapes with 1 and 2 dimensions.")
  console = rich.console.Console(width=max_width)
  use_color = use_color and console.color_system is not None
  if use_color and not color_map:
    try:
      import matplotlib as mpl  # pytype: disable=import-error
      color_map = mpl.colormaps["tab20b"]
    except ModuleNotFoundError:
      use_color = False

  base_height = int(10 * scale)
  aspect_ratio = (shape[1] if len(shape) == 2 else 1) / shape[0]
  base_width = int(base_height * aspect_ratio)
  height_to_width_ratio = 2.5

  # Grab the device kind from the first device
  device_kind = next(iter(sharding.device_set)).platform.upper()

  device_indices_map = sharding.devices_indices_map(tuple(shape))
  slices: dict[tuple[int, ...], set[int]] = {}
  heights: dict[tuple[int, ...], Optional[float]] = {}
  widths: dict[tuple[int, ...], float] = {}

  for i, (dev, slcs) in enumerate(device_indices_map.items()):
    assert slcs is not None
    slcs = tuple(map(_raise_to_slice, slcs))
    chunk_idxs = tuple(map(_slice_to_chunk_idx, shape, slcs))
    if slcs is None:
      raise NotImplementedError
    if len(slcs) == 2:
      vert, horiz = slcs
      vert_size  = ((vert.stop  - vert.start ) if vert.stop  is not None
                    else shape[0])
      horiz_size = ((horiz.stop - horiz.start) if horiz.stop is not None
                    else shape[1])
      chunk_height = vert_size / shape[0]
      chunk_width = horiz_size / shape[1]
      heights[chunk_idxs] = chunk_height
      widths[chunk_idxs] = chunk_width
    else:
      # In the 1D case, we set the height to 1.
      horiz, = slcs
      vert = slice(0, 1, None)
      horiz_size = (
          (horiz.stop - horiz.start) if horiz.stop is not None else shape[0])
      chunk_idxs = (0, *chunk_idxs)
      heights[chunk_idxs] = None
      widths[chunk_idxs]  = horiz_size / shape[0]
    slices.setdefault(chunk_idxs, set()).add(dev.id)
  num_rows = max([a[0] for a in slices.keys()]) + 1
  if len(list(slices.keys())[0]) == 1:
    num_cols = 1
  else:
    num_cols = max([a[1] for a in slices.keys()]) + 1

  color_iter = make_color_iter(color_map, num_rows, num_cols)
  table = rich.table.Table(show_header=False, show_lines=not use_color,
                           padding=0,
                           highlight=not use_color, pad_edge=False,
                           box=rich.box.SQUARE if not use_color else None)
  for i in range(num_rows):
    col = []
    for j in range(num_cols):
      entry = f"{device_kind} "+",".join([str(s) for s in sorted(slices[i, j])])
      width, maybe_height = widths[i, j], heights[i, j]
      width = int(width * base_width * height_to_width_ratio)
      if maybe_height is None:
        height = 1
      else:
        height = int(maybe_height * base_height)
      width = min(max(width, min_width), max_width)
      left_padding, remainder = divmod(width - len(entry) - 2, 2)
      right_padding = left_padding + remainder
      top_padding, remainder = divmod(height - 2, 2)
      bottom_padding = top_padding + remainder
      if use_color:
        color = _canonicalize_color(next(color_iter)[:3])
        text_color = _get_text_color(color)
        top_padding += 1
        bottom_padding += 1
        left_padding += 1
        right_padding += 1
      else:
        color = None
        text_color = None
      padding = (top_padding, right_padding, bottom_padding, left_padding)
      padding = tuple(max(x, 0) for x in padding)  # type: ignore
      col.append(
          rich.padding.Padding(
            rich.align.Align(entry, "center", vertical="middle"), padding,
            style=rich.style.Style(bgcolor=color,
              color=text_color)))
    table.add_row(*col)
  console.print(table, end='\n\n')
