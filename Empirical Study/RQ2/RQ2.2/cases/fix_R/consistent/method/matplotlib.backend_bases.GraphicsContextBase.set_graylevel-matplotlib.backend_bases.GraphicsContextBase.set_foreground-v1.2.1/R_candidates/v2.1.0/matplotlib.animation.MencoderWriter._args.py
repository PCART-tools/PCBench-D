    def _args(self):
        # Returns the command line parameters for subprocess to use
        # mencoder to create a movie
        return [self.bin_path(), '-', '-demuxer', 'rawvideo', '-rawvideo',
                ('w=%i:h=%i:' % self.frame_size +
                'fps=%i:format=%s' % (self.fps,
                                      self.frame_format))] + self.output_args
