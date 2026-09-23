def get_debugger() -> Debugger:
  debuggers = sorted(_debugger_registry.values(), key=lambda x: -x[0])
  if not debuggers:
    raise ValueError("No debuggers registered!")
  return debuggers[0][1]
