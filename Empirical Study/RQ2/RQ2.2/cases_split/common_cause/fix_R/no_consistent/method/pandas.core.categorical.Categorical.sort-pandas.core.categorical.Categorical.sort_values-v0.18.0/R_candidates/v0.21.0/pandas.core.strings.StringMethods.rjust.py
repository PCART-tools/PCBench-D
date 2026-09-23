    @Appender(_shared_docs['str_pad'] % dict(side='left', method='rjust'))
    def rjust(self, width, fillchar=' '):
        return self.pad(width, side='left', fillchar=fillchar)
