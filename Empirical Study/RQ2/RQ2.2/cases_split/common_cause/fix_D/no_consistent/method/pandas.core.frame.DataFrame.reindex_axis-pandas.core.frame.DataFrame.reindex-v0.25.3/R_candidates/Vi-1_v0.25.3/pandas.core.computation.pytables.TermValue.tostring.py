    def tostring(self, encoding):
        """ quote the string if not encoded
            else encode and return """
        if self.kind == "string":
            if encoding is not None:
                return self.converted
            return '"{converted}"'.format(converted=self.converted)
        elif self.kind == "float":
            # python 2 str(float) is not always
            # round-trippable so use repr()
            return repr(self.converted)
        return self.converted
