    @staticmethod
    def get_buf_from_file(f: IO[bytes]) -> bytes | mmap.mmap:
        if hasattr(f, "getbuffer"):
            return f.getbuffer()
        elif hasattr(f, "getvalue"):
            return f.getvalue()
        else:
            try:
                return mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            except ValueError:  # cannot mmap an empty file
                return b""
