    def load(self):
        if _webp.HAVE_WEBPANIM:
            if self.__loaded != self.__logical_frame:
                self._seek(self.__logical_frame)

                # We need to load the image data for this frame
                data, timestamp, duration = self._get_next()
                self.info["timestamp"] = timestamp
                self.info["duration"] = duration
                self.__loaded = self.__logical_frame

                # Set tile
                if self.fp and self._exclusive_fp:
                    self.fp.close()
                self.fp = BytesIO(data)
                self.tile = [("raw", (0, 0) + self.size, 0, self.rawmode)]

        return super().load()
