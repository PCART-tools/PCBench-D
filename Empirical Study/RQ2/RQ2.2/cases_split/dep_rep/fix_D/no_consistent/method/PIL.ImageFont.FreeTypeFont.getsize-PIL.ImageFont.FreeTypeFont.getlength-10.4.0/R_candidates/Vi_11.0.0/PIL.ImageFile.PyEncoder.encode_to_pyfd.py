    def encode_to_pyfd(self) -> tuple[int, int]:
        """
        If ``pushes_fd`` is ``True``, then this method will be used,
        and ``encode()`` will only be called once.

        :returns: A tuple of ``(bytes consumed, errcode)``.
            Err codes are from :data:`.ImageFile.ERRORS`.
        """
        if not self.pushes_fd:
            return 0, -8  # bad configuration
        bytes_consumed, errcode, data = self.encode(0)
        if data:
            assert self.fd is not None
            self.fd.write(data)
        return bytes_consumed, errcode
