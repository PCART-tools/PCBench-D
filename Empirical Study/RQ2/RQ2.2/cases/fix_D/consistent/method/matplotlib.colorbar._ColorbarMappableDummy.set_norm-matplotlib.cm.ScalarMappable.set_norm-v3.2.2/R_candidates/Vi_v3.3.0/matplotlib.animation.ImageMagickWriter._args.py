    def _args(self):
        return ([self.bin_path(),
                 '-size', '%ix%i' % self.frame_size, '-depth', '8',
                 '-delay', str(self.delay), '-loop', '0',
                 '%s:-' % self.frame_format]
                + self.output_args)
