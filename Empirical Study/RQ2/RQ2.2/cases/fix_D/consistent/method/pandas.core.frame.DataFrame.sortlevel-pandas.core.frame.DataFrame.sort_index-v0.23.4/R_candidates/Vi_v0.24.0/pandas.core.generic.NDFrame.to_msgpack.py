    def to_msgpack(self, path_or_buf=None, encoding='utf-8', **kwargs):
        """
        Serialize object to input file path using msgpack format.

        THIS IS AN EXPERIMENTAL LIBRARY and the storage format
        may not be stable until a future release.

        Parameters
        ----------
        path : string File path, buffer-like, or None
            if None, return generated string
        append : bool whether to append to an existing msgpack
            (default is False)
        compress : type of compressor (zlib or blosc), default to None (no
            compression)
        """

        from pandas.io import packers
        return packers.to_msgpack(path_or_buf, self, encoding=encoding,
                                  **kwargs)
