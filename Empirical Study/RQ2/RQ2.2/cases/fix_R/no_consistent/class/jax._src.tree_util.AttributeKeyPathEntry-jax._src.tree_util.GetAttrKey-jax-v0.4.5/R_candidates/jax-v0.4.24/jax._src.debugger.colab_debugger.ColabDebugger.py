class ColabDebugger(cli_debugger.CliDebugger):
  """A JAX debugger for a Colab environment."""

  def __init__(self,
               frames: list[debugger_core.DebuggerFrame],
               thread_id: int):
    super().__init__(frames, thread_id)
    self._debugger_view = DebuggerView(self.current_frame())
    self.stdout = self.stdin = self._debugger_view  # type: ignore

  def do_up(self, arg):
    super().do_up(arg)
    self._debugger_view.update_frame(self.current_frame())
    return False

  def do_down(self, arg):
    super().do_down(arg)
    self._debugger_view.update_frame(self.current_frame())
    return False

  def run(self):
    self._debugger_view.render()
    while True:
      if not self.cmdloop():
        return
