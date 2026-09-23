    def encode(self, encoding: TransferEncoding) -> Series:
        """
        Encode a value using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.

        Returns
        -------
        Series
            Series of data type :class:`Boolean`.

        """
