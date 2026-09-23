    def add_itxt(
        self,
        key: str | bytes,
        value: str | bytes,
        lang: str | bytes = "",
        tkey: str | bytes = "",
        zip: bool = False,
    ) -> None:
        """Appends an iTXt chunk.

        :param key: latin-1 encodable text key name
        :param value: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        :param zip: compression flag

        """

        if not isinstance(key, bytes):
            key = key.encode("latin-1", "strict")
        if not isinstance(value, bytes):
            value = value.encode("utf-8", "strict")
        if not isinstance(lang, bytes):
            lang = lang.encode("utf-8", "strict")
        if not isinstance(tkey, bytes):
            tkey = tkey.encode("utf-8", "strict")

        if zip:
            self.add(
                b"iTXt",
                key + b"\0\x01\0" + lang + b"\0" + tkey + b"\0" + zlib.compress(value),
            )
        else:
            self.add(b"iTXt", key + b"\0\0\0" + lang + b"\0" + tkey + b"\0" + value)
