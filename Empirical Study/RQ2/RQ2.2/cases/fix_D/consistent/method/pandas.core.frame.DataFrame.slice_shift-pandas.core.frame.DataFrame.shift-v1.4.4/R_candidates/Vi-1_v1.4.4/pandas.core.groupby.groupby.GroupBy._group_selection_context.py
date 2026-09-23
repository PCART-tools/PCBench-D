    @contextmanager
    def _group_selection_context(self) -> Iterator[GroupBy]:
        """
        Set / reset the _group_selection_context.
        """
        self._set_group_selection()
        try:
            yield self
        finally:
            self._reset_group_selection()
