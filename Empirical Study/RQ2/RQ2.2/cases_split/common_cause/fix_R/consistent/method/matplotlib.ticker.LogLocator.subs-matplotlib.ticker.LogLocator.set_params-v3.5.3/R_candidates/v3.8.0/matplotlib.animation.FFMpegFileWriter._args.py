    def _args(self):
        # Returns the command line parameters for subprocess to use
        # ffmpeg to create a movie using a collection of temp images
        args = []
        # For raw frames, we need to explicitly tell ffmpeg the metadata.
        if self.frame_format in {'raw', 'rgba'}:
            args += [
                '-f', 'image2', '-vcodec', 'rawvideo',
                '-video_size', '%dx%d' % self.frame_size,
                '-pixel_format', 'rgba',
            ]
        args += ['-framerate', str(self.fps), '-i', self._base_temp_name()]
        if not self._tmpdir:
            args += ['-frames:v', str(self._frame_counter)]
        # Logging is quieted because subprocess.PIPE has limited buffer size.
        # If you have a lot of frames in your animation and set logging to
        # DEBUG, you will have a buffer overrun.
        if _log.getEffectiveLevel() > logging.DEBUG:
            args += ['-loglevel', 'error']
        return [self.bin_path(), *args, *self.output_args]
