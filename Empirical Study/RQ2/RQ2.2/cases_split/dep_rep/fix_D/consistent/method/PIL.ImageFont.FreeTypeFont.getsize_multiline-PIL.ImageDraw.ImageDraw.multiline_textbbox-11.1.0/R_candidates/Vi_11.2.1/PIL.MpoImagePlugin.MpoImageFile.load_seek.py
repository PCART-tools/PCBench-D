    def load_seek(self, pos: int) -> None:
        if isinstance(self._fp, DeferredError):
            raise self._fp.ex
        self._fp.seek(pos)
