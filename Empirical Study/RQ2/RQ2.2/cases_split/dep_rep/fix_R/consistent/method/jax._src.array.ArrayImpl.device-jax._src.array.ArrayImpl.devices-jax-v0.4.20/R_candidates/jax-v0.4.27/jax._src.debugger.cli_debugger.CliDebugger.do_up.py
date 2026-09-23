  def do_up(self, _):
    """u(p)
    Move down a stack frame.
    """
    if self.frame_index == len(self.frames) - 1:
      print('At topmost frame.', file=self.stdout)
    else:
      self.frame_index += 1
    self.print_context()
