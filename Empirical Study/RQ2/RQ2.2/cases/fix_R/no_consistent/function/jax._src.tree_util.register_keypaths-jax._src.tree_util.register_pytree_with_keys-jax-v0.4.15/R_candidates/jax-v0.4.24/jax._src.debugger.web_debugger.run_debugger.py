def run_debugger(frames: list[debugger_core.DebuggerFrame],
                 thread_id: int | None, **kwargs: Any):
  WebDebugger(frames, thread_id, **kwargs).run()
