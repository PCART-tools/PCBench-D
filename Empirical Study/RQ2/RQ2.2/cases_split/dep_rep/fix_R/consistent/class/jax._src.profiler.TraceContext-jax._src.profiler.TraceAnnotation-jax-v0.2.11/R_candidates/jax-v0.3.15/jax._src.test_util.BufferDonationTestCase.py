class BufferDonationTestCase(JaxTestCase):
  assertDeleted = lambda self, x: self._assertDeleted(x, True)
  assertNotDeleted = lambda self, x: self._assertDeleted(x, False)

  def _assertDeleted(self, x, deleted):
    if hasattr(x, "device_buffer"):
      self.assertEqual(x.device_buffer.is_deleted(), deleted)
    else:
      for buffer in x.device_buffers:
        self.assertEqual(buffer.is_deleted(), deleted)
