def _read_most_recent_pjit_call_executable(jaxpr):
  return _most_recent_pjit_call_executable.weak_key_dict.get(jaxpr, None)
