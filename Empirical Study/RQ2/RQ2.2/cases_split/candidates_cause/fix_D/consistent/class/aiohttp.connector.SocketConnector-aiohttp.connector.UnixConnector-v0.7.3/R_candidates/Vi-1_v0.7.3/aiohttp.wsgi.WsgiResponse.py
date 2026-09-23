class WsgiResponse:
    """Implementation of start_response() callable as specified by PEP 3333"""

    status = None

    def __init__(self, writer, message):
        self.writer = writer
        self.message = message

    def start_response(self, status, headers, exc_info=None):
        if exc_info:
            try:
                if self.status:
                    raise exc_info[1]
            finally:
                exc_info = None

        status_code = int(status.split(' ', 1)[0])

        self.status = status
        resp = self.response = aiohttp.Response(
            self.writer, status_code,
            self.message.version, self.message.should_close)
        resp.add_headers(*headers)

        # send headers immediately for websocket connection
        if status_code == 101 and resp.upgrade and resp.websocket:
            resp.send_headers()
        else:
            resp._send_headers = True
        return self.response.write
