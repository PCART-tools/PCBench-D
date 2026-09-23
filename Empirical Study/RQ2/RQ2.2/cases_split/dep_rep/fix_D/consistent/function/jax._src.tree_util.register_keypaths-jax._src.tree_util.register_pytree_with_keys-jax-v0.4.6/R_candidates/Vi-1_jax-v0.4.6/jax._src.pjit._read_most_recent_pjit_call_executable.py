def _read_most_recent_pjit_call_executable():
  executable = _most_recent_pjit_call_executable.value
  _most_recent_pjit_call_executable.value = None
  return executable
