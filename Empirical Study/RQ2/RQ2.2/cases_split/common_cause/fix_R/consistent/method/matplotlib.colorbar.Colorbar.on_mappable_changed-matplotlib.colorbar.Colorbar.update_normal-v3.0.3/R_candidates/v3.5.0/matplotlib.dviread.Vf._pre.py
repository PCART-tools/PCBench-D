    def _pre(self, i, x, cs, ds):
        if self.state is not _dvistate.pre:
            raise ValueError("pre command in middle of vf file")
        if i != 202:
            raise ValueError("Unknown vf format %d" % i)
        if len(x):
            _log.debug('vf file comment: %s', x)
        self.state = _dvistate.outer
