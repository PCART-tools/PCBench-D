class Doc(util.StrictABC):
  __slots__ = ()

  def format(self, width: int = 80, use_color: bool | None = None,
             annotation_prefix=" # ") -> str:
    if use_color is None:
      use_color = CAN_USE_COLOR and _PPRINT_USE_COLOR.value
    return _format(self, width, use_color=use_color,
                   annotation_prefix=annotation_prefix)

  def __str__(self):
    return self.format()

  def __add__(self, other: Doc) -> Doc:
    return concat([self, other])
