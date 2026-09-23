class WebDebugger(cli_debugger.CliDebugger):
  """A web-based debugger."""
  prompt = '(jdb) '
  use_rawinput: bool = False

  def __init__(self, frames: list[debugger_core.DebuggerFrame], thread_id,
               completekey: str = "tab", host: str = "", port: int = 5555):
    if (host, port) not in _web_consoles:
      _web_consoles[host, port] = web_pdb.WebConsole(host, port, self)
    # Clobber the debugger in the web console
    _web_console = _web_consoles[host, port]
    _web_console._debugger = weakref.proxy(self)
    super().__init__(frames, thread_id, stdin=_web_console, stdout=_web_console,
                     completekey=completekey)

  def get_current_frame_data(self):
    # Constructs the info needed for the web console to display info
    current_frame = self.current_frame()
    filename = current_frame.filename
    lines = current_frame.source
    current_line = None
    if current_frame.offset is not None:
      current_line = current_frame.offset + 1
    if web_pdb_version and web_pdb_version < (1, 4, 4):
      return {
        'filename': filename,
        'listing': '\n'.join(lines),
        'curr_line': current_line,
        'total_lines': len(lines),
        'breaklist': [],
      }
    return {
        'dirname': os.path.dirname(os.path.abspath(filename)) + os.path.sep,
        'filename': os.path.basename(filename),
        'file_listing': '\n'.join(lines),
        'current_line': current_line,
        'breakpoints': [],
        'globals': self.get_globals(),
        'locals': self.get_locals(),
    }

  def get_globals(self):
    current_frame = self.current_frame()
    globals = "\n".join([f"{key} = {value}" for key, value in
      sorted(current_frame.globals.items())])
    return globals

  def get_locals(self):
    current_frame = self.current_frame()
    locals = "\n".join([f"{key} = {value}" for key, value in
      sorted(current_frame.locals.items())])
    return locals

  def run(self):
    return self.cmdloop()
