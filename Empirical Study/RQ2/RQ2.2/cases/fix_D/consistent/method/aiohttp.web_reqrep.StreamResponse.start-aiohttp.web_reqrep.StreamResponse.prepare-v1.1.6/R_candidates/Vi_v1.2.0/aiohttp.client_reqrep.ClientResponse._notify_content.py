    def _notify_content(self):
        content = self.content
        if content and content.exception() is None and not content.is_eof():
            content.set_exception(
                aiohttp.ClientDisconnectedError('Connection closed'))
