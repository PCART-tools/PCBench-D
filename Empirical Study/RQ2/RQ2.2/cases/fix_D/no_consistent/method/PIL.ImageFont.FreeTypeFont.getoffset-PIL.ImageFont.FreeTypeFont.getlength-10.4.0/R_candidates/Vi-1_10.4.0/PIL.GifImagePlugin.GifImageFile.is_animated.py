    @cached_property
    def is_animated(self) -> bool:
        if self._n_frames is not None:
            return self._n_frames != 1

        current = self.tell()
        if current:
            return True

        try:
            self._seek(1, False)
            is_animated = True
        except EOFError:
            is_animated = False

        self.seek(current)
        return is_animated
