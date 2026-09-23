class BufferDonationTestCase(JaxTestCase):
  def assertDeleted(self, x):
    self.assertTrue(x.is_deleted())

  def assertNotDeleted(self, x):
    self.assertFalse(x.is_deleted())
