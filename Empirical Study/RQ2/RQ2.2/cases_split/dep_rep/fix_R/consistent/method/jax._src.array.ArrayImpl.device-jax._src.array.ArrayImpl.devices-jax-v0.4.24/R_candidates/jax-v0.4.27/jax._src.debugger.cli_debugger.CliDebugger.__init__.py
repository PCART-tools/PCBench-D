  def __init__(self, frames: list[DebuggerFrame], thread_id,
      stdin: IO[str] | None = None, stdout: IO[str] | None = None,
      completekey: str = "tab"):
    super().__init__(stdin=stdin, stdout=stdout, completekey=completekey)
    self.use_rawinput = stdin is None
    self.frames = frames
    self.frame_index = 0
    self.thread_id = thread_id
    self.intro = 'Entering jdb:'
