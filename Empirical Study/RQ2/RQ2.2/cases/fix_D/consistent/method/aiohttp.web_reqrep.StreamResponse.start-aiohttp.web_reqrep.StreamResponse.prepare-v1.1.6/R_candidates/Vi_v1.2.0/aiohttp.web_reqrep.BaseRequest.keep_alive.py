    @property
    def keep_alive(self):
        """Is keepalive enabled by client?"""
        return not self._message.should_close
