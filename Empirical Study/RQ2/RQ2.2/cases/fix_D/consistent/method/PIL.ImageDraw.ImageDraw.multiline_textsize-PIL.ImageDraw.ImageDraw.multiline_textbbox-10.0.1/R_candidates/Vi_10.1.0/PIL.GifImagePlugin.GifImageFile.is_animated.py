    @property
    def is_animated(self):
        if self._is_animated is None:
            if self._n_frames is not None:
                self._is_animated = self._n_frames != 1
            else:
                current = self.tell()
                if current:
                    self._is_animated = True
                else:
                    try:
                        self._seek(1, False)
                        self._is_animated = True
                    except EOFError:
                        self._is_animated = False

                    self.seek(current)
        return self._is_animated
