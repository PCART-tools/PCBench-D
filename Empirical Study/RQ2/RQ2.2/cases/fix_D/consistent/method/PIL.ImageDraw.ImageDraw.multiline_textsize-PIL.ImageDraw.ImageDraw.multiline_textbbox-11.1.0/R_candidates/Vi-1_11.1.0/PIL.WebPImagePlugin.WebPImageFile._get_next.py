    def _get_next(self) -> tuple[bytes, int, int]:
        # Get next frame
        ret = self._decoder.get_next()
        self.__physical_frame += 1

        # Check if an error occurred
        if ret is None:
            self._reset()  # Reset just to be safe
            self.seek(0)
            msg = "failed to decode next frame in WebP file"
            raise EOFError(msg)

        # Compute duration
        data, timestamp = ret
        duration = timestamp - self.__timestamp
        self.__timestamp = timestamp

        # libwebp gives frame end, adjust to start of frame
        timestamp -= duration
        return data, timestamp, duration
