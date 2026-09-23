    def at_eof(self):
        """Returns ``True`` when all response data had been read.

        :rtype: bool
        """
        return self.resp.content.at_eof()
