    @dispatch(min=239, max=242, args=('ulen1',))
    def _xxx(self, datalen):
        special = self.file.read(datalen)
        if six.PY3:
            chr_ = chr
        else:
            def chr_(x):
                return x
        matplotlib.verbose.report(
            'Dvi._xxx: encountered special: %s'
            % ''.join([(32 <= ord(ch) < 127) and chr_(ch)
                       or '<%02x>' % ord(ch)
                       for ch in special]),
            'debug')
