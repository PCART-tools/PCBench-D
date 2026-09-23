    @property
    def output_args(self):
        args = []
        suffix = Path(self.outfile).suffix
        if suffix in {'.apng', '.avif', '.gif', '.webm', '.webp'}:
            self.codec = suffix[1:]
        else:
            args.extend(['-vcodec', self.codec])
        extra_args = (self.extra_args if self.extra_args is not None
                      else mpl.rcParams[self._args_key])
        # For h264, the default format is yuv444p, which is not compatible
        # with quicktime (and others). Specifying yuv420p fixes playback on
        # iOS, as well as HTML5 video in firefox and safari (on both Windows and
        # macOS). Also fixes internet explorer. This is as of 2015/10/29.
        if self.codec == 'h264' and '-pix_fmt' not in extra_args:
            args.extend(['-pix_fmt', 'yuv420p'])
        # For GIF, we're telling FFmpeg to split the video stream, to generate
        # a palette, and then use it for encoding.
        elif self.codec == 'gif' and '-filter_complex' not in extra_args:
            args.extend(['-filter_complex',
                         'split [a][b];[a] palettegen [p];[b][p] paletteuse'])
        # For AVIF, we're telling FFmpeg to split the video stream, extract the alpha,
        # in order to place it in a secondary stream, as needed by AVIF-in-FFmpeg.
        elif self.codec == 'avif' and '-filter_complex' not in extra_args:
            args.extend(['-filter_complex',
                         'split [rgb][rgba]; [rgba] alphaextract [alpha]',
                         '-map', '[rgb]', '-map', '[alpha]'])
        if self.bitrate > 0:
            args.extend(['-b', '%dk' % self.bitrate])  # %dk: bitrate in kbps.
        for k, v in self.metadata.items():
            args.extend(['-metadata', f'{k}={v}'])
        args.extend(extra_args)

        return args + ['-y', self.outfile]
