  def __init__(self, *args, axis_name, spmd_axis_name = None):
    super().__init__(*args)
    self.axis_name = axis_name
    self.spmd_axis_name = spmd_axis_name
