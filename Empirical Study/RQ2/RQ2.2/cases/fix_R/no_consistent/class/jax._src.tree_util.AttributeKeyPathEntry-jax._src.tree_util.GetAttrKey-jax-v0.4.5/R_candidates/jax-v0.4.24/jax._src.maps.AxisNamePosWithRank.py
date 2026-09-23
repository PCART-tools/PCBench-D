class AxisNamePosWithRank(AxisNamePos):
  def __init__(self, *args, expected_rank, **kwargs):
    super().__init__(*args, **kwargs)
    self.expected_rank = expected_rank
