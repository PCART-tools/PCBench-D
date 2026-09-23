def _layout_to_mlir_layout(minor_to_major: Sequence[int] | None):
  if minor_to_major is None:
    # Needed for token layouts
    layout = np.zeros((0,), dtype="int64")
  else:
    layout = np.array(minor_to_major, dtype="int64")
  return ir.DenseIntElementsAttr.get(layout, type=ir.IndexType.get())
