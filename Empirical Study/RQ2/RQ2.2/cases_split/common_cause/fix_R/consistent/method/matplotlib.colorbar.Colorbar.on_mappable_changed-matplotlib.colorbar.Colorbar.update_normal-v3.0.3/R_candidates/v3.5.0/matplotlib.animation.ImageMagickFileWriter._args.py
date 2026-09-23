    def _args(self):
        # Force format: ImageMagick does not recognize 'raw'.
        fmt = 'rgba:' if self.frame_format == 'raw' else ''
        return ([self.bin_path(),
                 '-size', '%ix%i' % self.frame_size, '-depth', '8',
                 '-delay', str(self.delay), '-loop', '0',
                 '%s%s*.%s' % (fmt, self.temp_prefix, self.frame_format)]
                + self.output_args)
