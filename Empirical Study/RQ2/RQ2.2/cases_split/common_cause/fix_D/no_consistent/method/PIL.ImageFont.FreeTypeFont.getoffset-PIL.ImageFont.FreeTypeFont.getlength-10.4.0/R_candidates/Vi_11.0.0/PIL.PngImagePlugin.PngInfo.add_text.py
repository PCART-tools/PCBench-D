    def add_text(
        self, key: str | bytes, value: str | bytes | iTXt, zip: bool = False
    ) -> None:
        """Appends a text chunk.

        :param key: latin-1 encodable text key name
        :param value: value for this key, text or an
           :py:class:`PIL.PngImagePlugin.iTXt` instance
        :param zip: compression flag

        """
        if isinstance(value, iTXt):
            return self.add_itxt(
                key,
                value,
                value.lang if value.lang is not None else b"",
                value.tkey if value.tkey is not None else b"",
                zip=zip,
            )

        # The tEXt chunk stores latin-1 text
        if not isinstance(value, bytes):
            try:
                value = value.encode("latin-1", "strict")
            except UnicodeError:
                return self.add_itxt(key, value, zip=zip)

        if not isinstance(key, bytes):
            key = key.encode("latin-1", "strict")

        if zip:
            self.add(b"zTXt", key + b"\0\0" + zlib.compress(value))
        else:
            self.add(b"tEXt", key + b"\0" + value)
