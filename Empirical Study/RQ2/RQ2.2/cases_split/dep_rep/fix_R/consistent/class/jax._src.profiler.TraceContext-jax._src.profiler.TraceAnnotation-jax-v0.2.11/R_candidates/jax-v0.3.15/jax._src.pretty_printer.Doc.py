class Doc(abc.ABC):
  __slots__ = ()

  def format(self, width: int = 80, use_color: Optional[bool] = None,
             annotation_prefix=" # ") -> str:
    if use_color is None:
      use_color = CAN_USE_COLOR and config.FLAGS.jax_pprint_use_color
    return _format(self, width, use_color=use_color,
                   annotation_prefix=annotation_prefix)

  def __str__(self):
    return self.format()

  def __add__(self, other: 'Doc') -> 'Doc':
    return concat([self, other])
