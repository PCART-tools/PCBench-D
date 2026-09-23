    def load(self) -> Image.core.PixelAccess | None:
        if self.tile:
            # We need to load the image data for this frame
            data, timescale, pts_in_timescales, duration_in_timescales = (
                self._decoder.get_frame(self.__frame)
            )
            self.info["timestamp"] = round(1000 * (pts_in_timescales / timescale))
            self.info["duration"] = round(1000 * (duration_in_timescales / timescale))

            if self.fp and self._exclusive_fp:
                self.fp.close()
            self.fp = BytesIO(data)

        return super().load()
