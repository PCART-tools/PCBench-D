    def _pre(self, i, x, cs, ds):
        if self.state != _dvistate.pre:
            raise ValueError("pre command in middle of vf file")
        if i != 202:
            raise ValueError("Unknown vf format %d" % i)
        if len(x):
            matplotlib.verbose.report('vf file comment: ' + x, 'debug')
        self.state = _dvistate.outer
