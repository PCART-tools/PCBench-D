  def do_down(self, arg):
    super().do_down(arg)
    self._debugger_view.update_frame(self.current_frame())
    return False
