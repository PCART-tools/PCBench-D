    @Appender(_shared_docs['str_pad'] % 'right')
    def ljust(self, width, fillchar=' '):
        return self.pad(width, side='right', fillchar=fillchar)
