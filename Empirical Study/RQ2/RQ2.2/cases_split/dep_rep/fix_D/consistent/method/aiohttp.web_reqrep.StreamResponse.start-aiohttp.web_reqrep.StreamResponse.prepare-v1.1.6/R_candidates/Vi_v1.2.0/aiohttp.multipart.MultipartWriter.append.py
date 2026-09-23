    def append(self, obj, headers=None):
        """Adds a new body part to multipart writer."""
        if isinstance(obj, self.part_writer_cls):
            if headers:
                obj.headers.update(headers)
            self.parts.append(obj)
        else:
            if not headers:
                headers = CIMultiDict()
            self.parts.append(self.part_writer_cls(obj, headers))
        return self.parts[-1]
