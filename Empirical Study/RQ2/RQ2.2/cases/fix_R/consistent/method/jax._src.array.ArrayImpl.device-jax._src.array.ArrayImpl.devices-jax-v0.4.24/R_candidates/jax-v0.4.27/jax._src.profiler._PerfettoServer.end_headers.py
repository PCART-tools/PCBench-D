  def end_headers(self):
    self.send_header('Access-Control-Allow-Origin', '*')
    return super().end_headers()
