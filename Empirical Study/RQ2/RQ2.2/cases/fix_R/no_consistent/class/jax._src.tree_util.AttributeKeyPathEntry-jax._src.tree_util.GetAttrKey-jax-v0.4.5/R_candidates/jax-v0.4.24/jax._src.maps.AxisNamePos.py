class AxisNamePos(FrozenDict):
  user_repr: str
  expected_rank: int | None = None

  def __init__(self, *args, user_repr, **kwargs):
    super().__init__(*args, **kwargs)
    self.user_repr = user_repr
