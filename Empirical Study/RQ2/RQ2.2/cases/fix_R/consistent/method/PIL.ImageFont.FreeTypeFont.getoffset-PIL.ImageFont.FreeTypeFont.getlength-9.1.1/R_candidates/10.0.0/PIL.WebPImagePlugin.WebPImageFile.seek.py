    def seek(self, frame):
        if not self._seek_check(frame):
            return

        # Set logical frame to requested position
        self.__logical_frame = frame
