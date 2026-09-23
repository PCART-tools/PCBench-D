    def _args(self):
        # Returns the command line parameters for subprocess to use
        # ffmpeg to create a movie using a collection of temp images
        return [self.bin_path(), '-r', str(self.fps),
                '-i', self._base_temp_name(),
                '-vframes', str(self._frame_counter)] + self.output_args
