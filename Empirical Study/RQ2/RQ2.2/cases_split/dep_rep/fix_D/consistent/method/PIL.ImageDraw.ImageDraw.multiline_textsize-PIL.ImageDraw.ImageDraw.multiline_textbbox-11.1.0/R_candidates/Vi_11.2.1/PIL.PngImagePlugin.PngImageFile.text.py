    @property
    def text(self) -> dict[str, str | iTXt]:
        # experimental
        if self._text is None:
            # iTxt, tEXt and zTXt chunks may appear at the end of the file
            # So load the file to ensure that they are read
            if self.is_animated:
                frame = self.__frame
                # for APNG, seek to the final frame before loading
                self.seek(self.n_frames - 1)
            self.load()
            if self.is_animated:
                self.seek(frame)
        assert self._text is not None
        return self._text
