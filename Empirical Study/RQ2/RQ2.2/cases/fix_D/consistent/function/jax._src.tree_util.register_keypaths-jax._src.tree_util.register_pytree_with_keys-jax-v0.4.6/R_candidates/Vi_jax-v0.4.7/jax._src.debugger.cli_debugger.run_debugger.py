def run_debugger(frames: List[DebuggerFrame], thread_id: Optional[int],
                 **kwargs: Any):
  CliDebugger(frames, thread_id, **kwargs).run()
