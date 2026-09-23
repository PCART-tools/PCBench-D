    @Appender(_interval_shared_docs["set_closed"] % _index_doc_kwargs)
    def set_closed(self, closed):
        if closed not in _VALID_CLOSED:
            msg = "invalid option for 'closed': {closed}"
            raise ValueError(msg.format(closed=closed))

        # return self._shallow_copy(closed=closed)
        array = self._data.set_closed(closed)
        return self._simple_new(array, self.name)
