  def do_GET(self):
    self.server.last_request = self.path
    return super().do_GET()
