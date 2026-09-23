    def send_str(self, data):
        if not isinstance(data, str):
            raise TypeError('data argument must be str (%r)' % type(data))
        return self._writer.send(data, binary=False)
