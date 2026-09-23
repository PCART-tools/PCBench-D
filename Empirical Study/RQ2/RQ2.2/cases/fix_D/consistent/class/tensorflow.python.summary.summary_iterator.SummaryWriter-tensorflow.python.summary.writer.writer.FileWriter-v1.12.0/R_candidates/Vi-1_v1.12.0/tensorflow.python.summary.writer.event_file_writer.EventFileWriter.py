class EventFileWriter(object):
  """Writes `Event` protocol buffers to an event file.

  The `EventFileWriter` class creates an event file in the specified directory,
  and asynchronously writes Event protocol buffers to the file. The Event file
  is encoded using the tfrecord format, which is similar to RecordIO.
  """

  def __init__(self, logdir, max_queue=10, flush_secs=120,
               filename_suffix=None):
    """Creates a `EventFileWriter` and an event file to write to.

    On construction the summary writer creates a new event file in `logdir`.
    This event file will contain `Event` protocol buffers, which are written to
    disk via the add_event method.

    The other arguments to the constructor control the asynchronous writes to
    the event file:

    *  `flush_secs`: How often, in seconds, to flush the added summaries
       and events to disk.
    *  `max_queue`: Maximum number of summaries or events pending to be
       written to disk before one of the 'add' calls block.

    Args:
      logdir: A string. Directory where event file will be written.
      max_queue: Integer. Size of the queue for pending events and summaries.
      flush_secs: Number. How often, in seconds, to flush the
        pending events and summaries to disk.
      filename_suffix: A string. Every event file's name is suffixed with
        `filename_suffix`.
    """
    self._logdir = str(logdir)
    if not gfile.IsDirectory(self._logdir):
      gfile.MakeDirs(self._logdir)
    self._event_queue = six.moves.queue.Queue(max_queue)
    self._ev_writer = pywrap_tensorflow.EventsWriter(
        compat.as_bytes(os.path.join(self._logdir, "events")))
    self._flush_secs = flush_secs
    self._sentinel_event = self._get_sentinel_event()
    if filename_suffix:
      self._ev_writer.InitWithSuffix(compat.as_bytes(filename_suffix))
    self._closed = False
    self._worker = _EventLoggerThread(self._event_queue, self._ev_writer,
                                      self._flush_secs, self._sentinel_event)

    self._worker.start()

  def _get_sentinel_event(self):
    """Generate a sentinel event for terminating worker."""
    return event_pb2.Event()

  def get_logdir(self):
    """Returns the directory where event file will be written."""
    return self._logdir

  def reopen(self):
    """Reopens the EventFileWriter.

    Can be called after `close()` to add more events in the same directory.
    The events will go into a new events file.

    Does nothing if the EventFileWriter was not closed.
    """
    if self._closed:
      self._worker = _EventLoggerThread(self._event_queue, self._ev_writer,
                                        self._flush_secs, self._sentinel_event)
      self._worker.start()
      self._closed = False

  def add_event(self, event):
    """Adds an event to the event file.

    Args:
      event: An `Event` protocol buffer.
    """
    if not self._closed:
      self._event_queue.put(event)

  def flush(self):
    """Flushes the event file to disk.

    Call this method to make sure that all pending events have been written to
    disk.
    """
    self._event_queue.join()
    self._ev_writer.Flush()

  def close(self):
    """Flushes the event file to disk and close the file.

    Call this method when you do not need the summary writer anymore.
    """
    self.add_event(self._sentinel_event)
    self.flush()
    self._worker.join()
    self._ev_writer.Close()
    self._closed = True
