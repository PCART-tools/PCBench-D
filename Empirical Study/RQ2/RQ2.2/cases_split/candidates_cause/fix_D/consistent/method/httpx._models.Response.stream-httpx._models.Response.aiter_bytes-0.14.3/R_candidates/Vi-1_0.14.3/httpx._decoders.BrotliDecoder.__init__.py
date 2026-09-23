    def __init__(self) -> None:
        if brotli is None:  # pragma: nocover
            raise ImportError(
                "Using 'BrotliDecoder', but the 'brotlipy' or 'brotli' library "
                "is not installed."
                "Make sure to install httpx using `pip install httpx[brotli]`."
            ) from None

        self.decompressor = brotli.Decompressor()
        self.seen_data = False
        if hasattr(self.decompressor, "decompress"):
            self._decompress = self.decompressor.decompress
        else:
            self._decompress = self.decompressor.process  # pragma: nocover
