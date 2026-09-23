    def create_wsgi_response(self, message):
        return WsgiResponse(self.writer, message)
