@contextmanager
def new_sublevel() -> Generator[None, None, None]:
  sublevel = Sublevel(len(thread_local_state.trace_state.substack))
  thread_local_state.trace_state.substack.append(sublevel)
  try:
    yield
  finally:
    thread_local_state.trace_state.substack.pop()

  if config.check_tracer_leaks.value:
    t = ref(sublevel)
    del sublevel
    if t() is not None:
      leaked_tracers = maybe_find_leaked_tracers(t())
      if leaked_tracers:
        raise leaked_tracer_error("sublevel", t(), leaked_tracers)
