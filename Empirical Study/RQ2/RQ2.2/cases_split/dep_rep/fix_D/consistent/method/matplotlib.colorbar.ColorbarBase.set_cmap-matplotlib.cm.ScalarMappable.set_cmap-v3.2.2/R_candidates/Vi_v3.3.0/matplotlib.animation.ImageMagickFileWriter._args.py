    def _args(self):
        return ([self.bin_path(), '-delay', str(self.delay), '-loop', '0',
                 '%s*.%s' % (self.temp_prefix, self.frame_format)]
                + self.output_args)
