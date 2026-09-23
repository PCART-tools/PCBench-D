  def __init__(self,
               frames: list[debugger_core.DebuggerFrame],
               thread_id: int):
    super().__init__(frames, thread_id)
    self._debugger_view = DebuggerView(self.current_frame())
    self.stdout = self.stdin = self._debugger_view  # type: ignore
