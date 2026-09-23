    def add_web_socket(self, web_socket):
        assert hasattr(web_socket, 'send_binary')
        assert hasattr(web_socket, 'send_json')

        self.web_sockets.add(web_socket)

        _, _, w, h = self.canvas.figure.bbox.bounds
        self.resize(w, h)
        self._send_event('refresh')
