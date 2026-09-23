    @Appender(_shared_docs['str_pad'] % dict(side='right', method='right'))
    def ljust(self, width, fillchar=' '):
        return self.pad(width, side='right', fillchar=fillchar)
