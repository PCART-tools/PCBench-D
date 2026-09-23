def run_debugger(frames: List[debugger_core.DebuggerFrame],
                 thread_id: Optional[int], **kwargs: Any):
  WebDebugger(frames, thread_id, **kwargs).run()
