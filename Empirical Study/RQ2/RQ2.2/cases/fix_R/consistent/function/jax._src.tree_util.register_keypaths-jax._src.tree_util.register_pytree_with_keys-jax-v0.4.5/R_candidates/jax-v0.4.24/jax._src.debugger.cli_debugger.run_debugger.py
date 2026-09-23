def run_debugger(frames: list[DebuggerFrame], thread_id: int | None,
                 **kwargs: Any):
  CliDebugger(frames, thread_id, **kwargs).run()
