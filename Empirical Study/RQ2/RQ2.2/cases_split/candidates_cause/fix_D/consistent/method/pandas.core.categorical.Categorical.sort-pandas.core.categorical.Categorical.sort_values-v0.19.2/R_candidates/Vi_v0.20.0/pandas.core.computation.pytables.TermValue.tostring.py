    def tostring(self, encoding):
        """ quote the string if not encoded
            else encode and return """
        if self.kind == u'string':
            if encoding is not None:
                return self.converted
            return '"%s"' % self.converted
        elif self.kind == u'float':
            # python 2 str(float) is not always
            # round-trippable so use repr()
            return repr(self.converted)
        return self.converted
