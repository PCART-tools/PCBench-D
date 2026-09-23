    def decode(self) -> bytes:
        try:
            filter = self.dictionary[b"Filter"]
        except KeyError:
            return self.buf
        if filter == b"FlateDecode":
            try:
                expected_length = self.dictionary[b"DL"]
            except KeyError:
                expected_length = self.dictionary[b"Length"]
            return zlib.decompress(self.buf, bufsize=int(expected_length))
        else:
            msg = f"stream filter {repr(filter)} unknown/unsupported"
            raise NotImplementedError(msg)
