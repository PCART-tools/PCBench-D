class CliDebugger(cmd.Cmd):
  """A text-based debugger."""
  prompt = '(jaxdb) '
  use_rawinput: bool = False

  def __init__(self, frames: List[DebuggerFrame], thread_id,
      stdin: Optional[IO[str]] = None, stdout: Optional[IO[str]] = None,
      completekey: str = "tab"):
    super().__init__(stdin=stdin, stdout=stdout, completekey=completekey)
    self.frames = frames
    self.frame_index = 0
    self.thread_id = thread_id
    self.intro = 'Entering jaxdb:'

  def current_frame(self):
    return self.frames[self.frame_index]

  def evaluate(self, expr):
    env = {}
    curr_frame = self.frames[self.frame_index]
    env.update(curr_frame.locals)
    return eval(expr, {}, env)

  def print_backtrace(self):
    self.stdout.write('Traceback:\n')
    for frame in self.frames[::-1]:
      self.stdout.write(f'  File "{frame.filename}", line {frame.lineno}\n')
      if frame.offset is None:
        self.stdout.write('    <no source>\n')
      else:
        line = frame.source[frame.offset]
        self.stdout.write(f'    {line}\n')

  def print_context(self, num_lines=2):
    curr_frame = self.frames[self.frame_index]
    self.stdout.write(f'> {curr_frame.filename}({curr_frame.lineno})\n')
    for i, line in enumerate(curr_frame.source):
      assert curr_frame.offset is not None
      if (curr_frame.offset - 1 - num_lines <= i <=
          curr_frame.offset + num_lines):
        if i == curr_frame.offset:
          self.stdout.write(f'->  {line}\n')
        else:
          self.stdout.write(f'    {line}\n')

  def do_p(self, arg):
    try:
      self.stdout.write(repr(self.evaluate(arg)) + "\n")
    except Exception:
      traceback.print_exc(limit=1)

  def do_u(self, arg):
    if self.frame_index == len(self.frames) - 1:
      self.stdout.write('At topmost frame.\n')
    else:
      self.frame_index += 1
    self.print_context()

  def do_d(self, arg):
    if self.frame_index == 0:
      self.stdout.write('At bottommost frame.\n')
    else:
      self.frame_index -= 1
    self.print_context()

  def do_l(self, arg):
    self.print_context(num_lines=5)

  def do_ll(self, arg):
    self.print_context(num_lines=5)

  def do_c(self, arg):
    return True

  def do_EOF(self, arg):
    sys.exit(0)

  def do_bt(self, arg):
    self.print_backtrace()

  def run(self):
    while True:
      try:
        self.cmdloop()
        break
      except KeyboardInterrupt:
        self.stdout.write('--KeyboardInterrupt--\n')
