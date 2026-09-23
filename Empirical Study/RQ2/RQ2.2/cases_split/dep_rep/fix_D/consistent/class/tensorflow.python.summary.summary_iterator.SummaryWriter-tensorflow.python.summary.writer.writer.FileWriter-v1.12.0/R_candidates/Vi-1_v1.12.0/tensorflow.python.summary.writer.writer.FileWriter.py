@tf_export("summary.FileWriter")
class FileWriter(SummaryToEventTransformer):
  """Writes `Summary` protocol buffers to event files.

  The `FileWriter` class provides a mechanism to create an event file in a
  given directory and add summaries and events to it. The class updates the
  file contents asynchronously. This allows a training program to call methods
  to add data to the file directly from the training loop, without slowing down
  training.

  When constructed with a `tf.Session` parameter, a `FileWriter` instead forms
  a compatibility layer over new graph-based summaries (`tf.contrib.summary`)
  to facilitate the use of new summary writing with pre-existing code that
  expects a `FileWriter` instance.
  """

  def __init__(self,
               logdir,
               graph=None,
               max_queue=10,
               flush_secs=120,
               graph_def=None,
               filename_suffix=None,
               session=None):
    """Creates a `FileWriter`, optionally shared within the given session.

    Typically, constructing a file writer creates a new event file in `logdir`.
    This event file will contain `Event` protocol buffers constructed when you
    call one of the following functions: `add_summary()`, `add_session_log()`,
    `add_event()`, or `add_graph()`.

    If you pass a `Graph` to the constructor it is added to
    the event file. (This is equivalent to calling `add_graph()` later).

    TensorBoard will pick the graph from the file and display it graphically so
    you can interactively explore the graph you built. You will usually pass
    the graph from the session in which you launched it:

    ```python
    ...create a graph...
    # Launch the graph in a session.
    sess = tf.Session()
    # Create a summary writer, add the 'graph' to the event file.
    writer = tf.summary.FileWriter(<some-directory>, sess.graph)
    ```

    The `session` argument to the constructor makes the returned `FileWriter` a
    compatibility layer over new graph-based summaries (`tf.contrib.summary`).
    Crucially, this means the underlying writer resource and events file will
    be shared with any other `FileWriter` using the same `session` and `logdir`,
    and with any `tf.contrib.summary.SummaryWriter` in this session using the
    the same shared resource name (which by default scoped to the logdir). If
    no such resource exists, one will be created using the remaining arguments
    to this constructor, but if one already exists those arguments are ignored.
    In either case, ops will be added to `session.graph` to control the
    underlying file writer resource. See `tf.contrib.summary` for more details.

    Args:
      logdir: A string. Directory where event file will be written.
      graph: A `Graph` object, such as `sess.graph`.
      max_queue: Integer. Size of the queue for pending events and summaries.
      flush_secs: Number. How often, in seconds, to flush the
        pending events and summaries to disk.
      graph_def: DEPRECATED: Use the `graph` argument instead.
      filename_suffix: A string. Every event file's name is suffixed with
        `suffix`.
      session: A `tf.Session` object. See details above.

    Raises:
      RuntimeError: If called with eager execution enabled.

    @compatibility(eager)
    `FileWriter` is not compatible with eager execution. To write TensorBoard
    summaries under eager execution, use `tf.contrib.summary` instead.
    @end_compatibility
    """
    if context.executing_eagerly():
      raise RuntimeError(
          "tf.summary.FileWriter is not compatible with eager execution. "
          "Use tf.contrib.summary instead.")
    if session is not None:
      event_writer = EventFileWriterV2(
          session, logdir, max_queue, flush_secs, filename_suffix)
    else:
      event_writer = EventFileWriter(logdir, max_queue, flush_secs,
                                     filename_suffix)
    super(FileWriter, self).__init__(event_writer, graph, graph_def)

  def __enter__(self):
    """Make usable with "with" statement."""
    return self

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Make usable with "with" statement."""
    self.close()

  def get_logdir(self):
    """Returns the directory where event file will be written."""
    return self.event_writer.get_logdir()

  def add_event(self, event):
    """Adds an event to the event file.

    Args:
      event: An `Event` protocol buffer.
    """
    self.event_writer.add_event(event)

  def flush(self):
    """Flushes the event file to disk.

    Call this method to make sure that all pending events have been written to
    disk.
    """
    self.event_writer.flush()

  def close(self):
    """Flushes the event file to disk and close the file.

    Call this method when you do not need the summary writer anymore.
    """
    self.event_writer.close()

  def reopen(self):
    """Reopens the EventFileWriter.

    Can be called after `close()` to add more events in the same directory.
    The events will go into a new events file.

    Does nothing if the EventFileWriter was not closed.
    """
    self.event_writer.reopen()
