    @property
    def output_args(self):
        args = []
        if not Path(self.outfile).suffix == '.gif':
            args.extend(['-vcodec', self.codec])
        extra_args = (self.extra_args if self.extra_args is not None
                      else mpl.rcParams[self._args_key])
        # For h264, the default format is yuv444p, which is not compatible
        # with quicktime (and others). Specifying yuv420p fixes playback on
        # iOS, as well as HTML5 video in firefox and safari (on both Win and
        # OSX). Also fixes internet explorer. This is as of 2015/10/29.
        if self.codec == 'h264' and '-pix_fmt' not in extra_args:
            args.extend(['-pix_fmt', 'yuv420p'])
        if self.bitrate > 0:
            args.extend(['-b', '%dk' % self.bitrate])  # %dk: bitrate in kbps.
        args.extend(extra_args)
        for k, v in self.metadata.items():
            args.extend(['-metadata', '%s=%s' % (k, v)])

        return args + ['-y', self.outfile]
