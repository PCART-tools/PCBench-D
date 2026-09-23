    def read(self, wkt):
        if not isinstance(wkt, (bytes, str)):
            raise TypeError
        return wkt_reader_read(self.ptr, force_bytes(wkt))
