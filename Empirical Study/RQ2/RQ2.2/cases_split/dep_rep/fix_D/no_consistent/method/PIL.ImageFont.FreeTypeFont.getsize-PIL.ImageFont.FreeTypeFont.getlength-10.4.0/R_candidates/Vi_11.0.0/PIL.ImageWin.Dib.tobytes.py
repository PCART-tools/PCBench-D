    def tobytes(self) -> bytes:
        """
        Copy display memory contents to bytes object.

        :return: A bytes object containing display data.
        """
        return self.image.tobytes()
