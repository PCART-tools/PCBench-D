class FileWriterCacheTest(test.TestCase):
  """FileWriterCache tests."""

  def _test_dir(self, test_name):
    """Create an empty dir to use for tests.

    Args:
      test_name: Name of the test.

    Returns:
      Absolute path to the test directory.
    """
    test_dir = os.path.join(self.get_temp_dir(), test_name)
    if os.path.isdir(test_dir):
      for f in glob.glob("%s/*" % test_dir):
        os.remove(f)
    else:
      os.makedirs(test_dir)
    return test_dir

  def test_cache(self):
    with ops.Graph().as_default():
      dir1 = self._test_dir("test_cache_1")
      dir2 = self._test_dir("test_cache_2")
      sw1 = writer_cache.FileWriterCache.get(dir1)
      sw2 = writer_cache.FileWriterCache.get(dir2)
      sw3 = writer_cache.FileWriterCache.get(dir1)
      self.assertEqual(sw1, sw3)
      self.assertFalse(sw1 == sw2)
      sw1.close()
      sw2.close()
      events1 = glob.glob(os.path.join(dir1, "event*"))
      self.assertTrue(events1)
      events2 = glob.glob(os.path.join(dir2, "event*"))
      self.assertTrue(events2)
      events3 = glob.glob(os.path.join("nowriter", "event*"))
      self.assertFalse(events3)

  def test_clear(self):
    with ops.Graph().as_default():
      dir1 = self._test_dir("test_clear")
      sw1 = writer_cache.FileWriterCache.get(dir1)
      writer_cache.FileWriterCache.clear()
      sw2 = writer_cache.FileWriterCache.get(dir1)
      self.assertFalse(sw1 == sw2)
