  def assertNotDeleted(self, x):
    self.assertFalse(x.is_deleted())
