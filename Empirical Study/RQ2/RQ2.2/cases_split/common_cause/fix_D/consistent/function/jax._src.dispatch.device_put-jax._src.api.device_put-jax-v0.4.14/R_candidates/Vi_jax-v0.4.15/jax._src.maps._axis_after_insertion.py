def _axis_after_insertion(axis, inserted_named_axes):
  for inserted_axis in sorted(inserted_named_axes.values()):
    if inserted_axis >= axis:
      break
    axis += 1
  return axis
