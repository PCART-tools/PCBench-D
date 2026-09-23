class _PerfettoServer(http.server.SimpleHTTPRequestHandler):
  """Handles requests from `ui.perfetto.dev` for the `trace.json`"""

  def end_headers(self):
    self.send_header('Access-Control-Allow-Origin', '*')
    return super().end_headers()

  def do_GET(self):
    self.server.last_request = self.path
    return super().do_GET()

  def do_POST(self):
    self.send_error(404, "File not found")
