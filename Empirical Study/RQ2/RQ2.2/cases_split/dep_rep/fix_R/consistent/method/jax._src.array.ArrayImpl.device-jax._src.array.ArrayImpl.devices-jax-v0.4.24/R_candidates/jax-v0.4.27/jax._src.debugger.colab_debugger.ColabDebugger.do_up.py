  def do_up(self, arg):
    super().do_up(arg)
    self._debugger_view.update_frame(self.current_frame())
    return False
