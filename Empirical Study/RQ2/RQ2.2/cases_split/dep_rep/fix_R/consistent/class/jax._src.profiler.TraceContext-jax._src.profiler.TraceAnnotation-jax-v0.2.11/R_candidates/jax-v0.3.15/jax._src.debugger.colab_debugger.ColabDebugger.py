class ColabDebugger(cli_debugger.CliDebugger):
  """A JAX debugger for a Colab environment."""

  def __init__(self,
               frames: List[debugger_core.DebuggerFrame],
               thread_id: int):
    super().__init__(frames, thread_id)
    self._debugger_view = DebuggerView(self.current_frame())

  def read(self):
    return self._debugger_view.read()

  def cmdloop(self, intro=None):
    self.preloop()
    stop = None
    while not stop:
      if self.cmdqueue:
        line = self.cmdqueue.pop(0)
      else:
        try:
          line = self.read()
        except EOFError:
          line = "EOF"
      line = self.precmd(line)
      stop = self.onecmd(line)
      stop = self.postcmd(stop, line)
    self.postloop()

  def do_u(self, _):
    if self.frame_index == len(self.frames) - 1:
      self.log("At topmost frame.")
      return False
    self.frame_index += 1
    self._debugger_view.update_frame(self.current_frame())
    return False

  def do_d(self, _):
    if self.frame_index == 0:
      self.log("At bottommost frame.")
      return False
    self.frame_index -= 1
    self._debugger_view.update_frame(self.current_frame())
    return False

  def do_bt(self, _):
    self.log("Traceback:")
    for frame in self.frames[::-1]:
      filename = frame.filename.strip()
      filename = filename or "<no filename>"
      self.log(f"  File: {filename}, line ({frame.lineno})")
      if frame.offset < len(frame.source):
        line = frame.source[frame.offset]
        self.log(f"    {line.strip()}")
      else:
        self.log(" ")

  def do_c(self, _):
    return True

  def do_q(self, _):
    return True

  def do_EOF(self, _):
    return True

  def do_p(self, arg):
    try:
      value = self.evaluate(arg)
      self.log(repr(value))
    except Exception:  # pylint: disable=broad-except
      self.log(traceback.format_exc(limit=1))
    return False

  do_pp = do_p

  def log(self, text):
    self._debugger_view.log(html.escape(text))

  def run(self):
    self._debugger_view.render()
    try:
      self.cmdloop()
    except KeyboardInterrupt:
      self.log("--Keyboard-Interrupt--")
      pass
    self._debugger_view.clear()
