    @frame_format.setter
    def frame_format(self, frame_format):
        if frame_format in self.supported_formats:
            self._frame_format = frame_format
        else:
            _api.warn_external(
                f"Ignoring file format {frame_format!r} which is not "
                f"supported by {type(self).__name__}; using "
                f"{self.supported_formats[0]} instead.")
            self._frame_format = self.supported_formats[0]
