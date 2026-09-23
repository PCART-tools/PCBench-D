    def decode(self, buffer: bytes | Image.SupportsArrayInterface) -> tuple[int, int]:
        """
        Override to perform the decoding process.

        :param buffer: A bytes object with the data to be decoded.
        :returns: A tuple of ``(bytes consumed, errcode)``.
            If finished with decoding return -1 for the bytes consumed.
            Err codes are from :data:`.ImageFile.ERRORS`.
        """
        msg = "unavailable in base decoder"
        raise NotImplementedError(msg)
