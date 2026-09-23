    def remove_callback(self, oid):
        """
        Remove a callback based on its observer id.

        See Also
        --------
        add_callback
        """
        try:
            del self._propobservers[oid]
        except KeyError:
            pass
