    @reify
    def keep_alive(self):
        """Is keepalive enabled by client?"""
        if self.version < HttpVersion10:
            return False
        else:
            return not self._message.should_close
