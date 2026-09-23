    @property
    def output_args(self):
        args = ['-vcodec', self.codec]
        # For h264, the default format is yuv444p, which is not compatible
        # with quicktime (and others). Specifying yuv420p fixes playback on
        # iOS,as well as HTML5 video in firefox and safari (on both Win and
        # OSX). Also fixes internet explorer. This is as of 2015/10/29.
        if self.codec == 'h264' and '-pix_fmt' not in self.extra_args:
            args.extend(['-pix_fmt', 'yuv420p'])
        # The %dk adds 'k' as a suffix so that ffmpeg treats our bitrate as in
        # kbps
        if self.bitrate > 0:
            args.extend(['-b', '%dk' % self.bitrate])
        if self.extra_args:
            args.extend(self.extra_args)
        for k, v in self.metadata.items():
            args.extend(['-metadata', '%s=%s' % (k, v)])

        return args + ['-y', self.outfile]
