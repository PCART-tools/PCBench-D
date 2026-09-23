    def _ensure_read(self, fp: IO[bytes], size: int) -> bytes:
        ret = fp.read(size)
        if len(ret) != size:
            msg = (
                "Corrupt EXIF data.  "
                f"Expecting to read {size} bytes but only got {len(ret)}. "
            )
            raise OSError(msg)
        return ret
