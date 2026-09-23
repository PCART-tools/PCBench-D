    def _args(self):
        # Returns the command line parameters for subprocess to use
        # mencoder to create a movie
        return [self.bin_path(),
                'mf://%s*.%s' % (self.temp_prefix, self.frame_format),
                '-frames', str(self._frame_counter), '-mf',
                'type=%s:fps=%d' % (self.frame_format,
                                    self.fps)] + self.output_args
