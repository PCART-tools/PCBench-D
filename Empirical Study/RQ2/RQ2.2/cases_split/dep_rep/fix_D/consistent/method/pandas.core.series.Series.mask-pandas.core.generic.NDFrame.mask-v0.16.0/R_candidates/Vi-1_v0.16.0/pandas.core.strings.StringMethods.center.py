    @Appender(_shared_docs['str_pad'] % 'left and right')
    def center(self, width, fillchar=' '):
        return self.pad(width, side='both', fillchar=fillchar)
