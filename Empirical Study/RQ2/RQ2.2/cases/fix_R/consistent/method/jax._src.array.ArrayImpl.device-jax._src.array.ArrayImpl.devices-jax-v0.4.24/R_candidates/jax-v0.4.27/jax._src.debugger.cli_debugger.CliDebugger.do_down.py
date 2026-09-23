  def do_down(self, _):
    """d(own)
    Move down a stack frame.
    """
    if self.frame_index == 0:
      print('At bottommost frame.', file=self.stdout)
    else:
      self.frame_index -= 1
    self.print_context()
