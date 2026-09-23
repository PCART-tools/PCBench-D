    def _summary(self, name=None) -> str_t:
        """
        Return a summarized representation.

        Parameters
        ----------
        name : str
            name to use in the summary representation

        Returns
        -------
        String with a summarized representation of the index
        """
        if len(self) > 0:
            head = self[0]
            if hasattr(head, "format") and not isinstance(head, str):
                head = head.format()
            elif needs_i8_conversion(self.dtype):
                # e.g. Timedelta, display as values, not quoted
                head = self._formatter_func(head).replace("'", "")
            tail = self[-1]
            if hasattr(tail, "format") and not isinstance(tail, str):
                tail = tail.format()
            elif needs_i8_conversion(self.dtype):
                # e.g. Timedelta, display as values, not quoted
                tail = self._formatter_func(tail).replace("'", "")

            index_summary = f", {head} to {tail}"
        else:
            index_summary = ""

        if name is None:
            name = type(self).__name__
        return f"{name}: {len(self)} entries{index_summary}"
