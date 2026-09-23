    @Appender(_shared_docs['str_pad'] % dict(side='left and right',
              method='center'))
    def center(self, width, fillchar=' '):
        return self.pad(width, side='both', fillchar=fillchar)
