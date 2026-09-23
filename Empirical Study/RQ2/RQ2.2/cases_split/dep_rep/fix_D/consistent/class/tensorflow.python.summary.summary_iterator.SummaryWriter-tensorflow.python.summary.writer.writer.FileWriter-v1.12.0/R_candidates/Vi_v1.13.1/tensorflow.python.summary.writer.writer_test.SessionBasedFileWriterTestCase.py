class SessionBasedFileWriterTestCase(FileWriterTestCase):
  """Tests for FileWriter behavior when passed a Session argument."""

  def _FileWriter(self, *args, **kwargs):
    if "session" not in kwargs:
      # Pass in test_session() as the session. It will be cached during this
      # test method invocation so that any other use of test_session() with no
      # graph should result in re-using the same underlying Session.
      with self.cached_session() as sess:
        kwargs["session"] = sess
        return writer.FileWriter(*args, **kwargs)
    return writer.FileWriter(*args, **kwargs)

  def _createTaggedSummary(self, tag):
    summary = summary_pb2.Summary()
    summary.value.add(tag=tag)
    return summary

  def testSharing_withOtherSessionBasedFileWriters(self):
    logdir = self.get_temp_dir()
    with session.Session() as sess:
      # Initial file writer
      writer1 = writer.FileWriter(session=sess, logdir=logdir)
      writer1.add_summary(self._createTaggedSummary("one"), 1)
      writer1.flush()

      # File writer, should share file with writer1
      writer2 = writer.FileWriter(session=sess, logdir=logdir)
      writer2.add_summary(self._createTaggedSummary("two"), 2)
      writer2.flush()

      # File writer with different logdir (shouldn't be in this logdir at all)
      writer3 = writer.FileWriter(session=sess, logdir=logdir + "-other")
      writer3.add_summary(self._createTaggedSummary("three"), 3)
      writer3.flush()

      # File writer in a different session (should be in separate file)
      time.sleep(1.1)  # Ensure filename has a different timestamp
      with session.Session() as other_sess:
        writer4 = writer.FileWriter(session=other_sess, logdir=logdir)
        writer4.add_summary(self._createTaggedSummary("four"), 4)
        writer4.flush()

      # One more file writer, should share file with writer1
      writer5 = writer.FileWriter(session=sess, logdir=logdir)
      writer5.add_summary(self._createTaggedSummary("five"), 5)
      writer5.flush()

    event_paths = iter(sorted(glob.glob(os.path.join(logdir, "event*"))))

    # First file should have tags "one", "two", and "five"
    events = summary_iterator.summary_iterator(next(event_paths))
    self.assertEqual("brain.Event:2", next(events).file_version)
    self.assertEqual("one", next(events).summary.value[0].tag)
    self.assertEqual("two", next(events).summary.value[0].tag)
    self.assertEqual("five", next(events).summary.value[0].tag)
    self.assertRaises(StopIteration, lambda: next(events))

    # Second file should have just "four"
    events = summary_iterator.summary_iterator(next(event_paths))
    self.assertEqual("brain.Event:2", next(events).file_version)
    self.assertEqual("four", next(events).summary.value[0].tag)
    self.assertRaises(StopIteration, lambda: next(events))

    # No more files
    self.assertRaises(StopIteration, lambda: next(event_paths))

    # Just check that the other logdir file exists to be sure we wrote it
    self.assertTrue(glob.glob(os.path.join(logdir + "-other", "event*")))

  def testSharing_withExplicitSummaryFileWriters(self):
    logdir = self.get_temp_dir()
    with session.Session() as sess:
      # Initial file writer via FileWriter(session=?)
      writer1 = writer.FileWriter(session=sess, logdir=logdir)
      writer1.add_summary(self._createTaggedSummary("one"), 1)
      writer1.flush()

      # Next one via create_file_writer(), should use same file
      writer2 = summary_ops_v2.create_file_writer(logdir=logdir)
      with summary_ops_v2.always_record_summaries(), writer2.as_default():
        summary2 = summary_ops_v2.scalar("two", 2.0, step=2)
      sess.run(writer2.init())
      sess.run(summary2)
      sess.run(writer2.flush())

      # Next has different shared name, should be in separate file
      time.sleep(1.1)  # Ensure filename has a different timestamp
      writer3 = summary_ops_v2.create_file_writer(logdir=logdir, name="other")
      with summary_ops_v2.always_record_summaries(), writer3.as_default():
        summary3 = summary_ops_v2.scalar("three", 3.0, step=3)
      sess.run(writer3.init())
      sess.run(summary3)
      sess.run(writer3.flush())

      # Next uses a second session, should be in separate file
      time.sleep(1.1)  # Ensure filename has a different timestamp
      with session.Session() as other_sess:
        writer4 = summary_ops_v2.create_file_writer(logdir=logdir)
        with summary_ops_v2.always_record_summaries(), writer4.as_default():
          summary4 = summary_ops_v2.scalar("four", 4.0, step=4)
        other_sess.run(writer4.init())
        other_sess.run(summary4)
        other_sess.run(writer4.flush())

        # Next via FileWriter(session=?) uses same second session, should be in
        # same separate file. (This checks sharing in the other direction)
        writer5 = writer.FileWriter(session=other_sess, logdir=logdir)
        writer5.add_summary(self._createTaggedSummary("five"), 5)
        writer5.flush()

      # One more via create_file_writer(), should use same file
      writer6 = summary_ops_v2.create_file_writer(logdir=logdir)
      with summary_ops_v2.always_record_summaries(), writer6.as_default():
        summary6 = summary_ops_v2.scalar("six", 6.0, step=6)
      sess.run(writer6.init())
      sess.run(summary6)
      sess.run(writer6.flush())

    event_paths = iter(sorted(glob.glob(os.path.join(logdir, "event*"))))

    # First file should have tags "one", "two", and "six"
    events = summary_iterator.summary_iterator(next(event_paths))
    self.assertEqual("brain.Event:2", next(events).file_version)
    self.assertEqual("one", next(events).summary.value[0].tag)
    self.assertEqual("two", next(events).summary.value[0].tag)
    self.assertEqual("six", next(events).summary.value[0].tag)
    self.assertRaises(StopIteration, lambda: next(events))

    # Second file should have just "three"
    events = summary_iterator.summary_iterator(next(event_paths))
    self.assertEqual("brain.Event:2", next(events).file_version)
    self.assertEqual("three", next(events).summary.value[0].tag)
    self.assertRaises(StopIteration, lambda: next(events))

    # Third file should have "four" and "five"
    events = summary_iterator.summary_iterator(next(event_paths))
    self.assertEqual("brain.Event:2", next(events).file_version)
    self.assertEqual("four", next(events).summary.value[0].tag)
    self.assertEqual("five", next(events).summary.value[0].tag)
    self.assertRaises(StopIteration, lambda: next(events))

    # No more files
    self.assertRaises(StopIteration, lambda: next(event_paths))
