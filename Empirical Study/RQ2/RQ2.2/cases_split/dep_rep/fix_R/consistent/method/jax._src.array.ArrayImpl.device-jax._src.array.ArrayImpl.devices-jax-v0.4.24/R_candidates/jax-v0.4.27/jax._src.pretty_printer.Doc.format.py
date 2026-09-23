  def format(
    self, width: int = 80, *, use_color: bool | None = None,
    annotation_prefix: str = " # ",
    source_map: list[list[tuple[int, int, Any]]] | None = None
  ) -> str:
    """
    Formats a pretty-printer document as a string.

    Args:
    source_map: for each line in the output, contains a list of
      (start column, end column, source) tuples. Each tuple associates a
      region of output text with a source.
    """
    if use_color is None:
      use_color = CAN_USE_COLOR and _PPRINT_USE_COLOR.value
    return _format(self, width, use_color=use_color,
                   annotation_prefix=annotation_prefix, source_map=source_map)
