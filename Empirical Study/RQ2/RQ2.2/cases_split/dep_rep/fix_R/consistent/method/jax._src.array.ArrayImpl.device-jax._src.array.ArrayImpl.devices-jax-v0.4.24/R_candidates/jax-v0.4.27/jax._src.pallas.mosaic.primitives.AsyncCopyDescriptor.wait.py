  def wait(self):
    if self.is_remote:
      self.wait_send()
    self.wait_recv()
