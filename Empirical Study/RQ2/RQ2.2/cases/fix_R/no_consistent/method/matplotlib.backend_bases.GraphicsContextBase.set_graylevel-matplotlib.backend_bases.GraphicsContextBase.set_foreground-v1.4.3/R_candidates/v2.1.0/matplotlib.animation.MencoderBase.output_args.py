    @property
    def output_args(self):
        self._remap_metadata()
        lavcopts = {'vcodec': self.codec}
        if self.bitrate > 0:
            lavcopts.update(vbitrate=self.bitrate)
        args = ['-o', self.outfile, '-ovc', 'lavc', '-lavcopts',
                ':'.join(itertools.starmap('{0}={1}'.format,
                                           lavcopts.items()))]
        if self.extra_args:
            args.extend(self.extra_args)
        if self.metadata:
            args.extend(['-info', ':'.join('%s=%s' % (k, v)
                         for k, v in six.iteritems(self.metadata)
                         if k in self.allowed_metadata)])
        return args
