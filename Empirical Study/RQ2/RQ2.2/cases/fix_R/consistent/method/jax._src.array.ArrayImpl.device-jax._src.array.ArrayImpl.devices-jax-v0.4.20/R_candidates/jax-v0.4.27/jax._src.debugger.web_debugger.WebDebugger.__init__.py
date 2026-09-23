  def __init__(self, frames: list[debugger_core.DebuggerFrame], thread_id,
               completekey: str = "tab", host: str = "", port: int = 5555):
    if (host, port) not in _web_consoles:
      import web_pdb  # pytype: disable=import-error
      _web_consoles[host, port] = web_pdb.WebConsole(host, port, self)
    # Clobber the debugger in the web console
    _web_console = _web_consoles[host, port]
    _web_console._debugger = weakref.proxy(self)
    super().__init__(frames, thread_id, stdin=_web_console, stdout=_web_console,
                     completekey=completekey)
