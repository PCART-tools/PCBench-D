    def close(self):
        """Close underlying connector.

        Release all acquired resources.
        """
        if not self.closed:
            self._connector.close()
            self._connector = None
        ret = helpers.create_future(self._loop)
        ret.set_result(None)
        return ret
