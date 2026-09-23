class _EventLoggerThread(threading.Thread):
  """Thread that logs events."""

  def __init__(self, queue, ev_writer, flush_secs, sentinel_event):
    """Creates an _EventLoggerThread.

    Args:
      queue: A Queue from which to dequeue events.
      ev_writer: An event writer. Used to log brain events for
       the visualizer.
      flush_secs: How often, in seconds, to flush the
        pending file to disk.
      sentinel_event: A sentinel element in queue that tells this thread to
        terminate.
    """
    threading.Thread.__init__(self)
    self.daemon = True
    self._queue = queue
    self._ev_writer = ev_writer
    self._flush_secs = flush_secs
    # The first event will be flushed immediately.
    self._next_event_flush_time = 0
    self._sentinel_event = sentinel_event

  def run(self):
    while True:
      event = self._queue.get()
      if event is self._sentinel_event:
        self._queue.task_done()
        break
      try:
        self._ev_writer.WriteEvent(event)
        # Flush the event writer every so often.
        now = time.time()
        if now > self._next_event_flush_time:
          self._ev_writer.Flush()
          # Do it again in two minutes.
          self._next_event_flush_time = now + self._flush_secs
      finally:
        self._queue.task_done()
