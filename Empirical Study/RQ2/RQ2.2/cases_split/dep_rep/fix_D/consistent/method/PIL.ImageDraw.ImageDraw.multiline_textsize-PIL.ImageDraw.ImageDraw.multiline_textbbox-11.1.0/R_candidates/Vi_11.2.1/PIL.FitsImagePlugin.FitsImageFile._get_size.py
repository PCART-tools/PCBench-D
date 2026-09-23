    def _get_size(
        self, headers: dict[bytes, bytes], prefix: bytes
    ) -> tuple[int, int] | None:
        naxis = int(headers[prefix + b"NAXIS"])
        if naxis == 0:
            return None

        if naxis == 1:
            return 1, int(headers[prefix + b"NAXIS1"])
        else:
            return int(headers[prefix + b"NAXIS1"]), int(headers[prefix + b"NAXIS2"])
